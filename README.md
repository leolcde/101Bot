# Persona - n8n + FastAPI + Postgres DB + Ollama

---

## Installation

### Prerequisite: Docker Compose v2

This project works best with Docker Compose v2 (`docker compose`).

Check your version:

```bash
docker compose version
```

If this command is missing and you only have `docker-compose` v1, install the Compose plugin for your distro.
Legacy Compose v1 can crash on recent Docker Engine versions with Python tracebacks like `KeyError: 'id'`.

### 1 - Clone the repo

```bash
git clone ...
```

---

### 3 - Prepare n8n data folder

````bash
mkdir n8n_data
sudo chown -R 1000:1000 n8n_data
````

---

### 5 - Launch the project

```bash
./run.sh
```
- n8n -> http://localhost:5678"
- pythonscript -> http://pythonscript:8000"
- ollama -> http://ollama:11435"

---

### 6 - Import the workflow into n8n

1. Open n8n
2. Create an account (note that for every new n8n docker image you run, you'll have to recreate an account).
3. Get the activation key n8n sent you by email and enter it in your account settings.
4. Click **Create Workflow**
5. Select the 3 small dots in the top right corner and then click **Import from File**
6. Select the `persona.json` file from the `workflow/` folder in the repo

