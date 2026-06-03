# Use DB

## Connect to the database

```bash
docker exec -it n8n-postgres psql -U n8n -d n8n_auth
```

## See tables

```sql
\dt
```

## Drop table

```sql
DROP TABLE IF EXISTS <table_name> CASCADE;
```