# Database CLI Interface
by Rajiv Shah (rss5527)

## Prerequisites
* Python 3.9+
* PostgreSQL

## Set Up
### Creating the Virtual Environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```
Note: On Windows, replace `pip3` and `python3` in future commands with `pip` and `python`, respectively.

### Installing Dependencies

```bash
pip3 install -r requirements.txt
```

## Running the Project
### Importing Data

Ensure PostgreSQL is running. The scripts assume the username and password are both `postgres` and PostgreSQL is running on `localhost:5432`.

Create the database
```bash
createdb hotels
```

Run the `import.py` script to import data into PostgresSQL:

```bash
python3 import.py
```

### Running the CLI

To launch the CLI, run the `main.py` script:

```bash
python3 main.py
```

Follow the on-screen prompts to interact with the CLI.
