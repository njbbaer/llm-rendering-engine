import pytest

from src.renderer import Renderer


@pytest.fixture
def template_str():
    with open("src/chat_template.yml", "r") as file:
        return file.read()


@pytest.fixture
def vars():
    return {
        "list_of_things": ["thing1", "thing2", "thing3"],
        "system_message": "This is the pre instructions system message.\n"
        "{%- for thing in list_of_things %}\n"
        "  - {{ thing }}\n"
        "{%- endfor %}",
        "pre_instructions": [
            {"text": "{{ system_message }}"},
            {
                "image_url": "https://example.com/system_image.png",
                "text": "This is the pre instructions image system message text.",
            },
        ],
        "post_instructions": [
            {"text": "This is the post instructions system message."}
        ],
        "messages": [
            {"role": "assistant", "text": "Hello User!"},
            {
                "role": "user",
                "text": "Hello Assistant!",
                "image_url": "https://example.com/user_image.png",
            },
        ],
    }


@pytest.fixture
def target_messages():
    return [
        {
            "role": "system",
            "content": "This is the pre instructions system message.\n"
            "  - thing1\n"
            "  - thing2\n"
            "  - thing3",
        },
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


def test_render(template_str, vars, target_messages):
    rendered_template = Renderer(vars).render(template_str)
    assert rendered_template == target_messages
