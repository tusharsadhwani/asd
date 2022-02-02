from typing import Literal, TypedDict
from flask import Flask

app = Flask(__name__)

User = TypedDict(
    "User",
    {
        "userid": int,
        "username": str,
        "gender": Literal["male", "female"],
    },
)


@app.get("/")
def hello() -> str:
    return "Hello, flask!"


@app.get("/user")
def get_user() -> User:
    return {
        "username": "tusharsadhwani",
        "userid": 123456,
        "gender": "male",
    }


if __name__ == "__main__":
    app.run(port=8000)
