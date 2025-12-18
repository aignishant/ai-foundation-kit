import pytest
from AIFoundationKit.rag.prompts.generic_prompts import get_generic_prompt
from langchain_core.prompts import ChatPromptTemplate


def test_get_generic_prompt_success():
    prompt = get_generic_prompt("json_extraction")
    assert isinstance(prompt, ChatPromptTemplate)

    prompt = get_generic_prompt("UNIVERSAL_SUMMARY")
    assert isinstance(prompt, ChatPromptTemplate)


def test_get_generic_prompt_case_insensitive():
    prompt = get_generic_prompt("RaG_qA")
    assert isinstance(prompt, ChatPromptTemplate)


def test_get_generic_prompt_not_found():
    with pytest.raises(ValueError) as excinfo:
        get_generic_prompt("nonexistent_prompt")
    assert "Prompt 'nonexistent_prompt' not found" in str(excinfo.value)
