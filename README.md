# README

This is a personal template for a simple FastAPI application. I wrote it to help consolidate and demonstrate concepts I learned while reading about the library. The template uses API keys to secure its endpoints, via FastAPI's `Depends()` function, and stores user information using a SQLite database. The `SQLModel` library is used as the API's ORM.

## Starting the API

```bash
# from the root of the repository
uvicorn app.main:app --reload
```

The API should start at `localhost:8000`, and be available for requests. The API's docs will be available at `localhost:8000/docs`.

An example request against the API's `/users` endpoint:

```bash
http get :8000/users x-api-key:af5as3sdl6j87slkaaj2j
```

```http
HTTP/1.1 200 OK
content-length: 58
content-type: application/json
date: Mon, 01 Apr 2024 01:16:34 GMT
server: uvicorn

[
    {
        "admin": 1,
        "email": "andrew@ndrewwm.com",
        "name": "Andrew"
    }
]
```
