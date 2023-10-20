# a streamlit application that shows a list of text paragraphs
# when click on each text paragraph, it becomes a text area to allow editing, also a input box will show below the text paragraph


import streamlit as st
import sys
import boto3
import json

def invoke_llm(user_prompt):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    prompt = f"""

Human: Write {user_prompt}

Assistant:"""
    
    print(prompt)
    try:
        response = client.invoke_model(
            body = bytes(json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 2048,
                "temperature": 1.0,
                "top_k": 250,
                "top_p": 1,
                "stop_sequences": [
                "\\n\\nHuman:"
                ],
                "anthropic_version": "bedrock-2023-05-31"
            }), 'utf-8'),
            #modelId = "anthropic.claude-v2",
            modelId = "anthropic.claude-instant-v1",
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
        

if "article" not in st.session_state: 
    st.session_state["article"] = []

if "editing_idx" not in st.session_state: 
    st.session_state["editing_idx"] = None

st.title("AI Writer")

article_prompt = st.text_area("What would you like to write?", placeholder="A short story about an unicorn")
if st.button("Write"):
    # Use langchain to invoke a Bedrock model to generate text based on article_prompt
    # Split the text into paragraphs and add it to session_state["article"]
    raw_article = invoke_llm(article_prompt)
    st.session_state["article"] = raw_article.split("\n\n")
    
    

# Add a devider
st.markdown("---")

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
            
st.markdown('---')
if st.button("Export finished article"):
    st.text_area("Finished article", value="\n\n".join(st.session_state["article"]))