# Persona - n8n + FastAPI

---

## Installation

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
docker-compose up -d --build
```
- n8n -> http://localhost:5678
- API FastAPI -> http://localhost:8000

---

### 6 - Import the workflow into n8n

1. Open n8n
2. Create an account (note that for every new n8n docker image you run, you'll have to recreate an account).
3. Get the activation key n8n sent you by email and enter it in your account settings.
4. Click **Create Workflow**
5. Select the 3 small dots in the top right corner and then click **Import from File**
6. Select the `persona.json` file from the `workflow/` folder in the repo
