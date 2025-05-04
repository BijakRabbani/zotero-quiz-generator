#%%
from pyzotero import zotero
import os
import pandas as pd
import datetime as dt
import streamlit as st
from streamlit import session_state as ss
import random



def extract_data(data_raw):
    data_clean = pd.DataFrame()
    for temp in data_raw:
        data_clean = pd.concat([data_clean, pd.Series(temp['data'])], axis=1)

    return data_clean.T

#% Get collection id
def get_target_collection_id(zot, collection_names):
    collection_raw = zot.collections()
    collection_clean = extract_data(collection_raw)
    collection_clean = collection_clean.set_index('name')
    collection_target = collection_clean.loc[collection_names, 'key']
    return collection_target

#% Get list of items given a collection
def get_items_data(zot, collection_names):
    collection_target = get_target_collection_id(zot, collection_names)
    items_data = pd.DataFrame()
    for name, collection_key in collection_target.items():
        items = zot.everything(zot.collection_items(collection_key))
        items_clean = extract_data(items)
        items_clean['collection'] = name
        items_clean['collection_id'] = collection_key
        items_data = pd.concat([items_data, items_clean])
    
    attachments_list = (
        items_data[~items_data['parentItem'].isna()]
        .groupby('parentItem')['key']
        .apply(lambda x : x.tolist())
    )
    items_data = items_data[items_data['itemType']!='attachment'].copy()
    items_data['attachment_id'] = items_data['key'].apply(lambda x : attachments_list[x])
    return items_data

#% Get list of annotation
def get_annotation_data(zot, last_update=None):
    if last_update is None:
        annotation_raw = zot.everything(zot.items(itemType='annotation'))
        annotation_data = extract_data(annotation_raw)
    else:
        item_date = dt.datetime.today()
        annotation_data = pd.DataFrame()
        while last_update < item_date:  
            annotation_raw = zot.items(itemType='annotation')
            annotation_clean = extract_data(annotation_raw)
            annotation_data = pd.concat([annotation_data, annotation_clean])
            item_date = dt.datetime.strptime(annotation_data['dateModified'].min(), '%Y-%m-%dT%H:%M:%SZ')
    return annotation_data



#% Filter annotation
def filter_highlights(annotation_data_raw, items_data):
    return annotation_data_raw[
        (annotation_data_raw['annotationType'] == 'highlight')
        & (annotation_data_raw['annotationColor'] == '#a28ae5')
        & (annotation_data_raw['parentItem'].isin(items_data['attachment_id'].sum()))
    ]


#% Get highlights
@st.cache_data
def get_highlights():
    # Initialize Zotero client
    zot = zotero.Zotero(os.environ['ZOTERO_LIBRARY_ID'], 'user', os.environ['ZOTERO_API_KEY']) # local=True for read access to local Zotero
    collection_names = ['Math','Statistics']

    # Get items data
    items_data = get_items_data(zot, collection_names)

    # Get annotation data
    annotation_data_raw = get_annotation_data(zot)

    # Filter highlights
    annotation_data_clean = filter_highlights(annotation_data_raw, items_data)

    # Assuming `annotation_data_clean` contains the highlights
    highlights = annotation_data_clean['annotationText'].tolist()
    return highlights


# Function to randomly shuffle highlights without repetition and include all elements
@st.cache_data
def get_randomized_highlights(highlights):
    ss.question_count = 0
    if not highlights:
        return []
    return random.sample(highlights, len(highlights))


# Function to clear cache
def clear_cache():
    get_items_data.cache_clear()
    get_annotation_data.cache_clear()
    get_randomized_highlights.cache_clear()