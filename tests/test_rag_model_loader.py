import pytest
from unittest.mock import MagicMock, patch
from AIFoundationKit.rag.model_loader import ModelLoader, GoogleProvider, GroqProvider
from AIFoundationKit.base.exception.custom_exception import ModelException


@pytest.fixture
def mock_api_key_manager():
    with patch("AIFoundationKit.rag.model_loader.ApiKeyManager") as MockManager:
        instance = MockManager.return_value
        instance.get.return_value = "dummy_key"
        yield instance


@pytest.fixture
def model_loader(mock_api_key_manager):
    return ModelLoader(config_dict={})


def test_register_provider(model_loader):
    mock_provider = MagicMock()
    model_loader.register_provider("custom", mock_provider)
    assert model_loader._providers["custom"] == mock_provider


def test_get_provider_not_found(model_loader):
    with pytest.raises(ModelException):
        model_loader._get_provider("nonexistent")


@patch("AIFoundationKit.rag.model_loader.ChatGoogleGenerativeAI")
def test_google_load_llm(mock_chat_google, model_loader):
    provider = GoogleProvider()
    llm = provider.load_llm(model_loader.api_key_mgr, {})
    mock_chat_google.assert_called_once()
    assert llm == mock_chat_google.return_value


@patch("AIFoundationKit.rag.model_loader.GoogleGenerativeAIEmbeddings")
def test_google_load_embedding(mock_google_embeddings, model_loader):
    provider = GoogleProvider()
    emb = provider.load_embedding(model_loader.api_key_mgr, {})
    mock_google_embeddings.assert_called_once()
    assert emb == mock_google_embeddings.return_value


@patch("AIFoundationKit.rag.model_loader.ChatGroq")
def test_groq_load_llm(mock_chat_groq, model_loader):
    provider = GroqProvider()
    llm = provider.load_llm(model_loader.api_key_mgr, {})
    mock_chat_groq.assert_called_once()
    assert llm == mock_chat_groq.return_value


def test_groq_load_embedding_raises(model_loader):
    provider = GroqProvider()
    with pytest.raises(ModelException):
        provider.load_embedding(model_loader.api_key_mgr, {})


def test_model_loader_load_llm(model_loader):
    with patch.object(GoogleProvider, "load_llm") as mock_load:
        model_loader.load_llm("google")
        mock_load.assert_called_once()


def test_model_loader_load_embeddings(model_loader):
    with patch.object(GoogleProvider, "load_embedding") as mock_load:
        model_loader.load_embeddings("google")
        mock_load.assert_called_once()
