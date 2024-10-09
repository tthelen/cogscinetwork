# Cogsci Network

## Felder

- Foto
- Vorname
- Nachname
- Pronomen* (Auswahl he/she/they/none, freie Angabe)
- Titel
- Wohnort Stadt
- Wohnort Land (Auswahl)

## Setting up the Django Project

### Installing Python dependencies:

Create a virtual environment:

```bash
python -m venv env
```

Activate the environment:

```bash
./env/Scripts/activate
```

Install the Python packages:

```bash
pip install -r requirements.txt
```

### Setting up the database

```bash
python manage.py migrate
```

Do this again after each code update!

### Running the development server

Start the Django development server:

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 in your browser to view the app.
