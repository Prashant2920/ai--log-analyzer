def transform(log):
    return [
        log["response_time"],
        log["status"],
    ]