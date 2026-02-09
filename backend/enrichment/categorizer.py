from enrichment.prompts import VIBE_PROMPT_TEMPLATE


def build_prompt(product_title: str, description: str) -> str:
    return VIBE_PROMPT_TEMPLATE.format(product_title=product_title, description=description)
