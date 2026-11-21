replies = iter([
    {"tool": "lookup_notice", "notice_id": "N-042"},
    {"answer": "The deadline is 30 November."},
])

requests = []

def scripted_model(messages):
    requests.append(list(messages))  # Save what the loop sent us
    return next(replies)             # Return the next prepared reply
