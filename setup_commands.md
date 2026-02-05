# Commands Used to Set Up the Project

## PostgreSQL Setup
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create database
createdb online_retail1

# Verify database
psql -l | grep online_retail1
```

## Python Environment
```bash
# Install dependencies
pip3 install pandas openpyxl sqlalchemy psycopg2-binary

# Run data loading script
python3 load_data.py
```

## n8n Setup
```bash
# Start n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  n8nio/n8n
```

## PostgreSQL Configuration in n8n
- Host: `host.docker.internal`
- Database: `online_retail1`
- User: `surendarsinghgarewal`
- Password: *********
- Port: `5432`
- SSL: `disable`
