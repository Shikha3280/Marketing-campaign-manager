import sqlite3
import os

# Database connection details
DB_NAME = os.getenv("DB_NAME", "Marketing campaign manager")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Shikha#03")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

# --- CRUD Operations for Campaigns ---

def create_campaign(name, budget, start_date, end_date, description, channels):
    """Creates a new campaign and its associated channels."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO campaigns (name, budget, start_date, end_date, description) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (name, budget, start_date, end_date, description)
        )
        campaign_id = cur.fetchone()[0]
        for channel in channels:
            cur.execute(
                "INSERT INTO channels (campaign_id, channel_type) VALUES (%s, %s);",
                (campaign_id, channel)
            )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating campaign: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def read_campaigns():
    """Retrieves all campaigns with their associated channels."""
    conn = get_db_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM campaigns;")
        campaigns_data = cur.fetchall()
        
        campaigns = []
        for campaign in campaigns_data:
            cur.execute("SELECT channel_type FROM channels WHERE campaign_id = %s;", (campaign[0],))
            channels = [row[0] for row in cur.fetchall()]
            campaigns.append({
                "id": campaign[0], "name": campaign[1], "budget": campaign[2],
                "start_date": campaign[3], "end_date": campaign[4],
                "description": campaign[5], "channels": channels
            })
        return campaigns
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error reading campaigns: {error}")
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

def update_campaign(campaign_id, name, budget, start_date, end_date, description, channels):
    """Updates an existing campaign and its channels."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE campaigns SET name = %s, budget = %s, start_date = %s, end_date = %s, description = %s WHERE id = %s;",
            (name, budget, start_date, end_date, description, campaign_id)
        )
        # First delete old channels
        cur.execute("DELETE FROM channels WHERE campaign_id = %s;", (campaign_id,))
        # Then insert new channels
        for channel in channels:
            cur.execute(
                "INSERT INTO channels (campaign_id, channel_type) VALUES (%s, %s);",
                (campaign_id, channel)
            )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating campaign: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def delete_campaign(campaign_id):
    """Deletes a campaign."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM campaigns WHERE id = %s;", (campaign_id,))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting campaign: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

# --- CRUD Operations for Customers ---

def create_customer(name, email, demographics):
    """Creates a new customer."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO customers (name, email, demographics) VALUES (%s, %s, %s);",
            (name, email, demographics)
        )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating customer: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def read_customers():
    """Retrieves all customers."""
    conn = get_db_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customers;")
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error reading customers: {error}")
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

def update_customer(customer_id, name, email, demographics):
    """Updates an existing customer."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE customers SET name = %s, email = %s, demographics = %s WHERE id = %s;",
            (name, email, demographics, customer_id)
        )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating customer: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def delete_customer(customer_id):
    """Deletes a customer."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE id = %s;", (customer_id,))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting customer: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

# --- CRUD Operations for Segments and Customer-Segment Association ---

def create_segment(segment_name, criteria):
    """Creates a new segment and returns its ID."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO segments (segment_name, criteria) VALUES (%s, %s) RETURNING id;",
            (segment_name, criteria)
        )
        segment_id = cur.fetchone()[0]
        conn.commit()
        return segment_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating segment: {error}")
        conn.rollback()
        return None
    finally:
        if conn:
            cur.close()
            conn.close()

def add_customers_to_segment(segment_id, customer_ids):
    """Adds customers to a specific segment."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        for customer_id in customer_ids:
            cur.execute(
                "INSERT INTO customer_segments (customer_id, segment_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;",
                (customer_id, segment_id)
            )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error adding customers to segment: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def read_segments():
    """Retrieves all segments and their associated customers."""
    conn = get_db_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, segment_name, criteria FROM segments;")
        segments_data = cur.fetchall()
        
        segments = []
        for segment_data in segments_data:
            segment_id = segment_data[0]
            cur.execute(
                "SELECT c.id, c.name FROM customers c JOIN customer_segments cs ON c.id = cs.customer_id WHERE cs.segment_id = %s;",
                (segment_id,)
            )
            customers = cur.fetchall()
            segments.append({
                "id": segment_id,
                "name": segment_data[1],
                "criteria": segment_data[2],
                "customers": customers
            })
        return segments
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error reading segments: {error}")
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

def delete_segment(segment_id):
    """Deletes a segment."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM segments WHERE id = %s;", (segment_id,))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting segment: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

# --- CRUD Operations for Performance Metrics ---

def log_performance_metric(campaign_id, emails_sent, emails_opened, clicks):
    """Inserts a new performance metric record for a campaign."""
    conn = get_db_connection()
    if conn is None: return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO performance_metrics (campaign_id, emails_sent, emails_opened, clicks) VALUES (%s, %s, %s, %s);",
            (campaign_id, emails_sent, emails_opened, clicks)
        )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error logging performance metric: {error}")
        conn.rollback()
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

def get_performance_metrics(campaign_id=None):
    """Retrieves performance metrics for a specific campaign or all campaigns."""
    conn = get_db_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        if campaign_id:
            cur.execute("SELECT * FROM performance_metrics WHERE campaign_id = %s ORDER BY timestamp;", (campaign_id,))
        else:
            cur.execute("SELECT * FROM performance_metrics ORDER BY timestamp;")
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error retrieving performance metrics: {error}")
        return []
    finally:
        if conn:
            cur.close()
            conn.close()

# --- Business Insights Functions ---

def get_total_campaign_budget():
    """Calculates the total budget of all campaigns."""
    conn = get_db_connection()
    if conn is None: return 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT SUM(budget) FROM campaigns;")
        result = cur.fetchone()[0]
        return result if result is not None else 0
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error getting total budget: {error}")
        return 0
    finally:
        if conn:
            cur.close()
            conn.close()

def get_average_clicks_per_campaign():
    """Calculates the average clicks per campaign."""
    conn = get_db_connection()
    if conn is None: return 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT AVG(clicks) FROM performance_metrics;")
        result = cur.fetchone()[0]
        return result if result is not None else 0
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error getting average clicks: {error}")
        return 0
    finally:
        if conn:
            cur.close()
            conn.close()
            
def get_most_successful_campaign():
    """Finds the campaign with the highest number of clicks."""
    conn = get_db_connection()
    if conn is None: return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.name, SUM(pm.clicks) AS total_clicks
            FROM campaigns c
            JOIN performance_metrics pm ON c.id = pm.campaign_id
            GROUP BY c.name
            ORDER BY total_clicks DESC
            LIMIT 1;
        """)
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error getting most successful campaign: {error}")
        return None
    finally:
        if conn:
            cur.close()
            conn.close()

def get_campaign_count():
    """Counts the total number of campaigns."""
    conn = get_db_connection()
    if conn is None: return 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM campaigns;")
        return cur.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error getting campaign count: {error}")
        return 0
    finally:
        if conn:
            cur.close()
            conn.close()

def get_max_min_metrics():
    """Gets the max and min values for emails sent, opened, and clicks."""
    conn = get_db_connection()
    if conn is None: return {}
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                MAX(emails_sent), MIN(emails_sent),
                MAX(emails_opened), MIN(emails_opened),
                MAX(clicks), MIN(clicks)
            FROM performance_metrics;
        """)
        results = cur.fetchone()
        if results is None:
            return {}
        return {
            'max_sent': results[0], 'min_sent': results[1],
            'max_opened': results[2], 'min_opened': results[3],
            'max_clicks': results[4], 'min_clicks': results[5]
        }
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error getting max/min metrics: {error}")
        return {}
    finally:
        if conn:
            cur.close()
            conn.close()