# TODO: encapsulate this into the llm

def writing_prompt(user_prompt):
    return f"""Write {user_prompt}. Only show me what you write, do NOT say something like "Here is an article:" or "Here is a story" in the beginning."""

def revise_prompt(user_prompt, current_paragraph):
    return f"""
Revise the following paragraph this way: {user_prompt}. Only output the revised paragraph. Do NOT say something like "Here is the revised paragraph:" in the beginning.
---
{current_paragraph}
---
"""

def overall_revise_prompt(user_prompt, current_paragraph):
    return f"""
Revise the whole article this way: {user_prompt}. Output the whole article, including the paragraphs that have not changed. Do NOT say something like "Here is the revised article:" in the beginnging.
---
{current_paragraph}
---
"""
