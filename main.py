# a streamlit application that shows a list of text paragraphs
# when click on each text paragraph, it becomes a text area to allow editing, also a input box will show below the text paragraph


import streamlit as st
import pandas as pd
import numpy as np


if "article" not in st.session_state: 
    st.session_state["article"] = [
    "This is the first paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph",
    "This is the second paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is",
    "This is the third paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text paragraph. It is a text" 
    ]

if "editing_idx" not in st.session_state: 
    st.session_state["editing_idx"] = None

st.title("AI Writer")

def update_paragraph(new_value):
    print(editing_text_area)
    print(new_value)
    st.session_state["article"][idx] = editing_text_area
    st.session_state["editing_idx"] = None

for idx, paragraph in enumerate(st.session_state["article"]):
    if idx == st.session_state["editing_idx"]:
        editing_text_area = st.text_area("(Editing)", 
            value=paragraph, 
            #on_change=update_paragraph
        )
        if editing_text_area != st.session_state["article"][idx] or st.button("^ save", key=f"edit-{idx}"):
            st.session_state["article"][idx] = editing_text_area
            st.session_state["editing_idx"] = None
            st.rerun()
    else:
        paragraph
    # when the paragraph is clicked, turn the text into a text area with the paragraph as placeholder
        if st.button("^ edit", key=f"edit-{idx}"):
            st.session_state["editing_idx"] = idx
            st.rerun()
