# Marketing-campaign-manager
Of course. Here is a README.md file for the "Digital Ad Campaign Tracker" application. It provides a clear overview, setup instructions, and a guide to the application's features.

📊 Digital Ad Campaign Tracker
This is a Python-based application designed to help marketing professionals manage, track, and analyze digital ad campaigns. It features a user-friendly interface built with Streamlit and a robust backend powered by PostgreSQL.

✨ Features
Campaign Management: Create, update, and delete marketing campaigns with specified budgets, durations, and channels.

Customer Segmentation: Manage a database of customers and create dynamic segments for targeted messaging.

Performance Tracking: Log and view real-time performance metrics like emails sent, emails opened, and clicks.

Business Insights: A dedicated dashboard provides key insights using aggregate functions (SUM, COUNT, AVG, MAX, MIN) to help you understand campaign performance.

📁 Project Structure
The application is structured into two main files to follow the principle of separation of concerns:

frontend_mar.py: Handles the entire user interface using the Streamlit library. It presents forms, tables, and charts and calls the backend functions to process data.

backend_mar.py: Contains all the backend logic, including functions to connect to the PostgreSQL database via psycopg2 and perform all CRUD (Create, Read, Update, Delete) operations.

🚀 Getting Started
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.7+

PostgreSQL database server

1. Database Setup
First, you need to set up the PostgreSQL database and tables.

Open your PostgreSQL client (like psql or pgAdmin).

Create a new database:

SQL

CREATE DATABASE digital_ad_campaign_tracker;
Connect to the new database and run the schema script provided below to create all necessary tables:

SQL

-- campaigns table
CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    budget DECIMAL(10, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT
);

-- channels table
CREATE TABLE channels (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    channel_type VARCHAR(50) NOT NULL
);

-- customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    demographics TEXT
);

-- segments table
CREATE TABLE segments (
    id SERIAL PRIMARY KEY,
    segment_name VARCHAR(255) NOT NULL,
    criteria TEXT
);

-- many-to-many relationship for customer segments
CREATE TABLE customer_segments (
    customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE,
    segment_id INTEGER REFERENCES segments(id) ON DELETE CASCADE,
    PRIMARY KEY (customer_id, segment_id)
);

-- performance_metrics table
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES campaigns(id) ON DELETE CASCADE,
    emails_sent INTEGER DEFAULT 0,
    emails_opened INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Update the database connection details in backend_mar.py to match your local PostgreSQL credentials (e.g., DB_USER, DB_PASSWORD).

2. Install Python Dependencies
Make sure you have all the required Python libraries by installing them with pip:

Bash

pip install streamlit psycopg2 pandas
3. Run the Application
With the database set up and dependencies installed, you can start the application from your terminal:

Bash

streamlit run frontend_mar.py
The application will automatically open in your default web browser. You're ready to start tracking your campaigns!

🤝 Contribution
This project is a small-scale demonstration of database application development. Feel free to fork the repository and contribute to its enhancement.
