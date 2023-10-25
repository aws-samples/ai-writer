# a streamlit application that shows a list of text paragraphs
# when click on each text paragraph, it becomes a text area to allow editing, also a input box will show below the text paragraph


import streamlit as st
import sys
import boto3
import json
import re

from prompts import *
import config

def invoke_llm(prompt):
    client = boto3.client('bedrock-runtime', region_name=config.AWS_REGION)
    
    try:
        response = client.invoke_model(
            body = bytes(json.dumps({
                "prompt": prompt,
                **config.MODEL_PARAMETERS
            }), 'utf-8'),
            modelId = config.MODEL_ID,
            contentType = "application/json",
            accept = "application/json"
        )
        response_text = response['body'].read().decode('utf8').strip()
        response_json = json.loads(response_text)
        completion = response_json['completion']
        return completion
    except Exception as e:
        print('Error invoking endpoint')
        print(e)
        raise Exception("Error invoking LLM")

def split_paragraphs(full_article):
    # split the full_article into an array of paragraphs by a new line, but keep markdown code blocks wrapped by three backquotes in one paragraph
    paragraphs = full_article.splitlines(True)
    output = []
    in_code_block = False
    for paragraph in paragraphs:
        if in_code_block:
            if "```" in paragraph:
                in_code_block = False
            output[-1] += paragraph
            continue
        elif paragraph.startswith("```"):
            in_code_block = True
            output.append(paragraph)
            continue
        elif paragraph.strip() != "":
            output.append(paragraph)
    return output
            

if "article" not in st.session_state: 
    st.session_state["article"] = []

if "editing_idx" not in st.session_state: 
    st.session_state["editing_idx"] = None

# Start of layout
st.title("AI Writer")

is_starting_over = len(st.session_state["article"]) == 0

with st.expander("Start over", expanded = is_starting_over):
    article_prompt = st.text_area("What would you like to write?", placeholder="A short story about an unicorn")
    
    if st.button("Write"):
        # Use langchain to invoke a Bedrock model to generate text based on article_prompt
        # Split the text into paragraphs and add it to session_state["article"]
        raw_article = invoke_llm(writing_prompt(article_prompt))
        st.session_state["article"] = split_paragraphs(raw_article)
        st.rerun()
        
with st.expander("Revise the whole article", expanded = not is_starting_over):
    overall_revise_instruction = st.text_area("How would you like to revise the whole article?", placeholder="Change from third-person to first-person")
    if st.button("Revise"):
        revised_article = invoke_llm(overall_revise_prompt(overall_revise_instruction, "\n\n".join(st.session_state["article"])))
        st.session_state["article"] = split_paragraphs(revised_article)
    

# Add a devider
st.markdown("---")

for idx, paragraph in enumerate(st.session_state["article"]):
    if idx == st.session_state["editing_idx"]:
        st.markdown("---")
        text_col, action_col = st.columns([0.8, 0.2])
        with text_col:
            editing_text_area = st.text_area("(Editing)", 
                value=paragraph, 
                #on_change=update_paragraph
            )
        with action_col:
            if editing_text_area != st.session_state["article"][idx] or st.button("Save", key=f"edit-{idx}"):
                st.session_state["article"][idx] = editing_text_area
                st.session_state["editing_idx"] = None
                st.session_state["article"] = split_paragraphs("\n".join(st.session_state["article"])) # One paragraph might be edited to two
                st.rerun()
            revise_instruction= st.text_area("How would you like to revise this paragraph?", placeholder="Make the tone softer")
            if st.button("Revise", key=f"revise-{idx}"):
                revised_paragraph = invoke_llm(revise_prompt(revise_instruction, editing_text_area))
                st.session_state["article"][idx] = revised_paragraph
                st.session_state["article"] = split_paragraphs("\n".join(st.session_state["article"])) # One paragraph might be edited to two
                st.rerun()
        st.markdown("---")
            
            
    else:
        text_col, action_col_1, action_col_2 = st.columns([0.8, 0.1, 0.12])
        with text_col:
            paragraph
    # when the paragraph is clicked, turn the text into a text area with the paragraph as placeholder
        with action_col_1:
            if st.button("edit", key=f"edit-{idx}"):
                st.session_state["editing_idx"] = idx
                st.rerun()
        with action_col_2:
            if st.button("Delete", key=f"delete-{idx}"):
                st.session_state["article"].pop(idx)
                st.rerun()
            
st.markdown('---')
st.markdown("## Copy the article below")
st.text_area("Finished article", value="\n".join(st.session_state["article"]))