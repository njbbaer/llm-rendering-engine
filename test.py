from jinja2 import Template

template = "This is the pre instructions system message.\n{% for thing in list_of_things %}\n  - {{ thing }}\n{% endfor %}"
vars = {
    "list_of_things": ["thing1", "thing2", "thing3"],
    "system_message": "This is the pre instructions system message.\n{% for thing in list_of_things %}\n  - {{ thing }}\n{% endfor %}",
    "pre_instructions": [
        {"text": "{{ system_message }}"},
        {
            "image_url": "https://example.com/system_image.png",
            "text": "This is the pre instructions image system message text.",
        },
    ],
    "post_instructions": [{"text": "This is the post instructions system message."}],
    "messages": [
        {"role": "assistant", "text": "Hello User!"},
        {
            "role": "user",
            "text": "Hello Assistant!",
            "image_url": "https://example.com/user_image.png",
        },
    ],
}
print(Template(template).render(vars))
