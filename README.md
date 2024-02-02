# py-rest-template

A Python RESTful FastAPI template with SQLite database and session handling.

## Features

- Uses [FastAPI](https://fastapi.tiangolo.com/) for the API
- Uses [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- Uses [SQLModel](https://sqlmodel.tiangolo.com/) for database models and
  migrations
- Uses [SQLite](https://www.sqlite.org/index.html) for the database
- Prioritizes asynchronous code for better performance (with `aiosqlite`)
- Contains a basic user authentication system with login and registration
    - Includes password hashing with PBKDF2 using `hashlib`
- Contains [hurl](https://hurl.dev) tests for the API (in `tests/`)

## Usage

It is recommended to use Nix with Flakes for development. If you have Nix
installed, you can simply run `nix develop` to enter a development environment
with all the necessary dependencies.

Once you have the development environment set up, you can run the following
commands:

```sh
# Install the project dependencies
pip install -r requirements.txt

# Run the server
./main.py
```

You may also choose to run the server with `uvicorn` for hot-reloading:

```sh
uvicorn main:app --reload
```

## License

This project is licensed under the terms of the ISC license. See the
[LICENSE](LICENSE) file for details.
