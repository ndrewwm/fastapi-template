# Overview

This is a template that can be used to deploy a REST API (implemented using FastAPI) with the following characteristics:

- API functionality organized into routes
- endpoints secured using API keys
- database management using [SQLModel](https://sqlmodel.tiangolo.com/)
- cryptographic hashing of user credentials using `pyargon`

# Template Conventions

- Endpoint routes will avoid using trailing-slashes.

- Route names will use `snake_case`.

- Pagination parameters are `limit` and `offset`.

- The HTTP method(s) for an endpoint should reflect the operation. For example, an endpoint in which the end-user is expected to provide a JSON payload should have the operation be designated as a POST. Updates to a resource should be designated as PATCH operations. Operations where data is being uploaded and may replace an existing resource should use PUT. Requests to determine the current state of a resource should use GET. Requests to delete an existing resource should use DELETE.

- Endpoints (routes), models, and schemas should be organized as Python modules. Each module should be focused on delivering a specific feature (or highly related set of features).

- For its repository, the template uses the following application structure:
  - `./app`: global modules, including `main`. Core features that can be defined as their own file should be implemented here, using a single descriptive filename (such as "auth", or "database").
  - `./app/docs`: markdown files that might feed into sections of the API's documentation.
  - `./app/models`: Contains data models that the API uses. Preference is to have one file per model, although it might be appropriate to have 2+ *highly related* models defined in the same module.
  - `./app/routes`: Each set of endpoints related to a specific business/application purpose should be located within their own module. For complex logic, a sub-folder with related modules can be placed within `/routes`.
  - `./app/schemas`: Schemas for JSON data returned by the API.

# Why did I make this?

I wanted to consolidate some personal learning I've made FastAPI, and hopefully speed up the process of building out an application that needs a simple API in which it's desirable or tolerable to maintain the codebase in Python. As a library, FastAPI is new(er), but has **two highly attractive aspects:**

1. The developer experience of writing an API feels very smooth. Using `pydantic` to validate inputs (and handle conflicts) feels very natural. I'm spending much less time thinking about exceptions, and letting existing patterns do a lot of work for me. The code I end up writing for a method feels more compact and cleaner.

2. It's hard to overstate how valuable it is to autogenerate documentation that updates alongside your application's code. FastAPI makes standing up **documentation** for an API almost seamless. The fact that I can render an OpenAPI schema out of the box, with virtually everything filled out by work I was already doing in 1. is **super cool.**
