import pytest

from src.executor import execute
from src.updaters import chat_updater


@pytest.fixture
def template_str():
    with open("src/chat_template.yml", "r") as file:
        return file.read()


@pytest.fixture
def vars():
    return {
        "pre_instructions": [
            {"text": "This is the pre instructions system message."},
            {
                "image_url": "https://example.com/system_image.png",
                "text": "This is the pre instructions image system message text.",
            },
        ],
        "post_instructions": [
            {"text": "This is the post instructions system message."}
        ],
    }


@pytest.fixture
def context():
    return {
        "messages": [
            {"role": "assistant", "text": "Hello User!"},
            {
                "role": "user",
                "text": "Hello Assistant!",
                "image_url": "https://example.com/user_image.png",
            },
        ]
    }


@pytest.fixture
def target_messages():
    return [
        {"role": "system", "content": "This is the pre instructions system message."},
        {
            "role": "system",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/system_image.png",
                        "detail": "low",
                    },
                },
                {
                    "type": "text",
                    "text": "This is the pre instructions image system message text.",
                },
            ],
        },
        {"role": "assistant", "content": "Hello User!"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/user_image.png",
                        "detail": "low",
                    },
                },
                {"type": "text", "text": "Hello Assistant!"},
            ],
        },
        {"role": "system", "content": "This is the post instructions system message."},
    ]


@pytest.fixture
def mock_openai(mocker):
    mock_create = mocker.Mock(
        return_value=mocker.Mock(
            choices=[mocker.Mock(message=mocker.Mock(content="AI response"))]
        )
    )
    return mocker.patch(
        "openai.OpenAI",
        return_value=mocker.Mock(
            chat=mocker.Mock(completions=mocker.Mock(create=mock_create))
        ),
    )


def test_execute_chat(template_str, vars, context, target_messages, mock_openai):
    output_json = execute(template_str, vars, context, chat_updater)
    _, called_kwargs = mock_openai.return_value.chat.completions.create.call_args
    assert called_kwargs["messages"] == target_messages
    assert output_json["messages"][-1]["content"] == "AI response"
