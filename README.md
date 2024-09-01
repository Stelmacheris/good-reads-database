# GoodReads Best Books Database

This repository contains the script to generate database to ingest csv data for GoodReads Best Books. The data was sourced from Kaggle and is structured according to an Entity-Relationship Diagram (ERD) included in the repository. The database is managed using PostgreSQL.

## Dataset URL

[GoodReads Best Books Dataset (kaggle.com)](https://www.kaggle.com/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b)

## Entity-Relationship Diagram

![alt text](https://i.postimg.cc/cCCHCh9M/erd.jpg)

## Prerequisites

Before you begin, ensure you have the following installed:

- PostgreSQL (Version 12.0 or newer recommended)
- pgAdmin 4 (or another PostgreSQL client)
- Python 3.8 or newer
- pip (Python package installer)

## Installation Guide

### 1. Clone the Repository

Start by cloning this repository to your local machine using:

```bash
git clone https://github.com/TuringCollegeSubmissions/martstelm-DE1.v2.3.5.git
cd martstelm-DE1.v2.3.5
```

### 2. Set Up Python Environment

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Create database

Then, create a new database in PostgreSQL:

```sql
CREATE DATABASE good_reads_books;
```

### 4. Configure Environment Variables

Create a .env file in the src directory of your project and add the following environment variables to configure your database connection:

```bash
cd src/
```

```env
DB_NAME=good_reads_books
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
```

### 5. Run application

Copy csv file into src folder and run python application

```bash
python main.py
```

### 6. Verify the Import

To verify that the data has been imported successfully, you can run the following SQL query:

```sql
SELECT *
FROM public.all_good_books_info
LIMIT 10;
```

## Usage

You can now use pgAdmin or any other PostgreSQL client to connect to the `good_reads_books` database and run queries, generate reports, or perform analysis.
