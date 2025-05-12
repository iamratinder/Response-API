from langchain_core.prompts import PromptTemplate
import random

def initial_prompt() -> PromptTemplate:
    return PromptTemplate(
        template="Tell me a {random_style} joke about {topic}. Make it short, witty, and unpredictable.",
        input_variables=['random_style', 'topic']
    )

def final_prompt() -> PromptTemplate:
    return PromptTemplate(
        template=(
        """You are a super creative comedy writer.
        Take this {random_style} joke and rewrite it to make it even more original, absurd, or clever,
        but keep the same topic {topic}.
        Only output the joke and don't mention something like it's rewritten or anything:\n{joke}"""
        ),
        input_variables=["random_style", "topic", "joke"]
    )



