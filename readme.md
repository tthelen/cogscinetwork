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

### Building Tailwind CSS (requires [Node.js](https://nodejs.org/en))

Process `raw_tailwind_input.css` styles to `global_tailwind.css`. The latter is references in the base html template.

The process looks at styles from `templates/.../.html|.js` and removes (purges) all unusued styles from the output. Only styles that were used are included in the `global_tailwind.css` file. (see `content` option in `tailwind.config.js`)

```bash
npm run build-css
```

File watcher, processes `global_tailwind.css` on html file save.

```bash
npm run watch-css
```