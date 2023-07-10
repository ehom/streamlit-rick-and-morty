import platform
import re
import requests
import sys
import streamlit as st
import time

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4, width=40)

BASE_URL = "https://rickandmortyapi.com/api/character"

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = BASE_URL
    st.session_state['next_page'] = None
    st.session_state['prev_page'] = None
    st.session_state['pages'] = None
    st.session_state['cache'] = {}


def get_page_from(url):
    search_results = re.search(r"page=(\d+)", st.session_state['current_page'])
    if search_results:
        # print("current_page:", search_results)
        # print("current_page part 1:", search_results[0])
        # print("current_page part 2:", search_results[1])
        current_page = search_results[1]
    else:
        current_page = 1
    return current_page


class Model():
    # TODO cache data so that we don't have
    # to fetch over the network all the time
    # 
    # For now, cache everything. 
    # Later, evict entries


    def fetch_data():
        print(st.session_state['current_page'])
        current_page = get_page_from(st.session_state['current_page'])
        print("current page:", current_page) 

        if current_page in st.session_state['cache']:
            print("Found it in the cache!")
            return st.session_state.cache[current_page] 
        else:
            print("Cache page!")
            response = requests.get(st.session_state['current_page'])
            object = response.json() if response.ok else None
            st.session_state.cache[current_page] = object
            return object


def render_view(object):
    # print("render_view:")
    # pp.pprint(object)

    st.sidebar.title("Ricky and Morty API Test Drive")
    st.sidebar.caption("work in progress...")
    st.sidebar.divider()
    st.sidebar.markdown(f"* Streamlit {st.__version__}")
    st.sidebar.markdown(f"* Python {platform.python_version()}")

    st.session_state['next_page'] = object['info']['next']
    st.session_state['prev_page'] = object['info']['prev']
    st.session_state['pages'] = object['info']['pages']

    st.title("Rick and Morty characters")

    # print("current page:", st.session_state['current_page'])

    current_page = get_page_from(st.session_state['current_page'])

    cols = st.columns(5)

    with cols[0]:
        disable_prev = st.session_state['prev_page'] is None
        st.button("Previous Page", disabled=disable_prev, on_click=get_prev_page)

    with cols[2]:
        message = "{} of {}".format(current_page, st.session_state['pages'])
        st.write(message)

    with cols[4]:
        disable_next = st.session_state['next_page'] is None
        st.button("Next Page", disabled=disable_next, on_click=get_next_page)

    chars = object["results"]
    for i in range(0, len(chars), 5):
        chunk = object['results'][i:i+5]
        cols = st.columns(5)
        try:
            for n in range(0, 5):
                with cols[n]:
                    st.image(chunk[n]['image'], width=100)
        except Exception as e:
            print("An error occurred:", e)


def get_prev_page():
    st.session_state['current_page'] = st.session_state['prev_page']


def get_next_page():
    st.session_state['current_page'] = st.session_state['next_page']


def main():
    time_start = time.time()
    data = Model.fetch_data()
    time_end = time.time()
    print("Fetch data took ", time_end - time_start)

    render_view(data)


if __name__ == "__main__":
    main()
