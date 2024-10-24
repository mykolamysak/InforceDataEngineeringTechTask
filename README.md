# Data Engineering ETL Pipeline Project

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline that processes user data from a CSV file and loads it into a PostgreSQL database. The pipeline includes data validation, transformation, and various SQL queries for data analysis. The entire application is containerized using Docker for easy deployment and execution.

## Navigation
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Quick Start](#quick-start)
- [ETL Pipeline Details](#etl-pipeline-details)
  - [Data Extraction](#1-data-extraction)
  - [Data Transformation](#2-data-transformation)
  - [Data Loading](#3-data-loading)
- [SQL Queries](#sql-queries)
- [Environment Variables](#environment-variables)
- [Assumptions and Decisions](#assumptions-and-decisions)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites
- Docker
- Docker Compose

## Project Structure
```
InforceDataEngineeringTechTask/
├── data/
│   ├── updated_user_data.csv
│   └── user_data.csv
│
├── sql/
│   ├── 1_CountUsersSignedUpEachDay.sql
│   ├── 2_UniqueEmailDomains.sql
│   ├── 3_SignedUpLast7Days.sql
│   ├── 4_MostCommonEmailDomain.sql
│   └── 5_DeleteWhereDomain.sql
│
├── src/
│   ├── constants.py
│   ├── file_handler.py
│   ├── main.py
│   └── sql_handler.py
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── config.ini
├── LICENSE
├── requirements.txt
└── README.md
```

## Database Schema
```sql
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    signup_date DATE NOT NULL,
    domain VARCHAR(255) NOT NULL
);
```

## Quick Start
1. Clone the repository:
```bash
git clone https://github.com/mykolamysak/InforceDataEngineeringTechTask
cd InforceDataEngineeringTechTas
```

2. Start the application:
```bash
docker-compose up --build -d
```

This will:
- Build the Docker containers
- Initialize the PostgreSQL database
- Run the ETL pipeline
- Execute the SQL queries

## ETL Pipeline Details

### 1. Data Extraction
- Reads user data from a CSV file containing user_id, name, email, and signup_date
- CSV file contains over 1000 records
- Data is validated during extraction

### 2. Data Transformation
The pipeline performs the following transformations:
- Converts signup_date to YYYY-MM-DD format
- Validates email addresses
- Extracts domain names from email addresses
- Filters out invalid records

### 3. Data Loading
- Automatically creates the required database table
- Loads transformed data into PostgreSQL
- Handles data type conversions and constraints

## SQL Queries

The following queries are available in the `sql/` directory:

1. `1_CountUsersSignedUpEachDay.sql`: Count of users who signed up on each day
2. `2_UniqueEmailDomains.sql`: List of all unique email domains
3. `3_SignedUpLast7Days.sql`: Users who signed up in the last 7 days
4. `4_MostCommonEmailDomain.sql`: Users with the most common email domains
5. `5_DeleteWhereDomain.sql`: Filter records to keep only specific email domains

## Environment Variables
The following environment variables can be configured in compose.yml`:

```yaml
POSTGRES_USER: postgres
POSTGRES_PASSWORD: your_password
POSTGRES_DB: user_db
```

## Assumptions and Decisions
1. Email Validation:
   - Emails must contain @ symbol
   - Domain must have at least one period
   - Local part must not be empty

2. Data Processing:
   - Duplicate user_ids are rejected
   - Empty names are not allowed
   - Signup dates must be valid dates
   - Invalid records are logged but not loaded

3. Performance:
   - Batch processing is used for database insertions
   - Indexes are created on frequently queried columns

## Troubleshooting
1. If containers fail to start:
```bash
docker-compose down -v
docker-compose up --build
```

2. To check logs:
```bash
docker-compose logs -f
```

3. To access the PostgreSQL database directly:
```bash
docker exec -it postgres-container psql -U postgres -d user_db
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.