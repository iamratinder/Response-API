from langchain_core.prompts import PromptTemplate

def setup_joke_template() -> PromptTemplate:
    return PromptTemplate(
        template="""You are a professional comedian specialized in crafting clever and family-friendly jokes. Your jokes should be witty and engaging.
        Tell me a clean, clever joke about {topic}""",
        input_variables=["topic"],
        validate_template=True
    )






