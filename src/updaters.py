def chat_updater(context, response):
    context["messages"].append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    return context
