from fastapi import Request


def log(tag="MyApp", message="Hello", request: Request = None):
    with open("log.txt", "a+") as log:
        log.write(f"{tag}: {message}\n")
        log.write(f"URL: {request.url}\n")
