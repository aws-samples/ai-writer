# a streamlit application that shows a list of text paragraphs
# when click on each text paragraph, it becomes a text area to allow editing, also a input box will show below the text paragraph


import streamlit as st
import sys
import boto3
import json

def writing_prompt(user_prompt):
    return f"""

Human: Write {user_prompt}. Only show me what you write, do NOT say something like "Here is an article:" or "Here is a story" in the beginning.

Assistant:"""

def revise_prompt(user_prompt, current_paragraph):
    return f"""

Human: Revise the following paragraph this way: {user_prompt}. Only output the revised paragraph.
---
{current_paragraph}
---

Assistant:"""

def invoke_llm(prompt):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    
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
    raw_article = invoke_llm(writing_prompt(article_prompt))
    st.session_state["article"] = raw_article.split("\n\n")
with st.expander("Start over"):
    "Are you sure you want to remove everything that has been written?"
    if st.button("Yes"):
        print("Cleaning")
        st.session_state["article"] = []
    
overall_revise_prompt = st.text_area("How would you like to revise the whole article?", placeholder="Change from third-person to first-person")
if st.button("Revise"):
    revised_article = invoke_llm(revise_prompt(overall_revise_prompt, "\n\n".join(st.session_state["article"])))
    st.session_state["article"] = revised_article.split("\n\n")
    

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
        revise_instruction= st.text_area("How would you like to revise this paragraph?", placeholder="Make the tone softer")
        if st.button("Revise", key=f"revise-{idx}"):
            revised_paragraph = invoke_llm(revise_prompt(revise_instruction, editing_text_area))
            st.session_state["article"][idx] = revised_paragraph
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