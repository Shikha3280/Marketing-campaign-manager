import streamlit as st
import pandas as pd
from datetime import date
import backend_mar as bm

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Digital Ad Campaign Tracker")

# App Title and Description
st.title("Digital Ad Campaign Tracker 📊")
st.markdown("A simple application to manage marketing campaigns, track performance, and gain business insights.")

# --- Helper Functions for Frontend ---

def show_campaign_form(campaign_data=None):
    """Displays the form for creating or updating a campaign."""
    with st.form("campaign_form", clear_on_submit=True):
        st.subheader("Campaign Details")
        name = st.text_input("Campaign Name", value=campaign_data.get('name', '') if campaign_data else '')
        budget = st.number_input("Budget", min_value=0.0, value=float(campaign_data.get('budget', 0)) if campaign_data else 0.0)
        start_date = st.date_input("Start Date", value=campaign_data.get('start_date', date.today()) if campaign_data else date.today())
        end_date = st.date_input("End Date", value=campaign_data.get('end_date', date.today()) if campaign_data else date.today())
        description = st.text_area("Description", value=campaign_data.get('description', '') if campaign_data else '')
        
        all_channels = ['Email', 'Social Media', 'Paid Ads']
        selected_channels = st.multiselect(
            "Channels",
            options=all_channels,
            default=campaign_data.get('channels', []) if campaign_data else ['Email']
        )
        
        submitted = st.form_submit_button("Submit Campaign")
        if submitted:
            if campaign_data:
                # Update existing campaign
                if bm.update_campaign(campaign_data['id'], name, budget, start_date, end_date, description, selected_channels):
                    st.success("Campaign updated successfully!")
                else:
                    st.error("Failed to update campaign.")
            else:
                # Create new campaign
                if bm.create_campaign(name, budget, start_date, end_date, description, selected_channels):
                    st.success("New campaign created successfully!")
                else:
                    st.error("Failed to create campaign.")
            st.rerun()

# --- Main Streamlit App Layout ---

# Sidebar for navigation
st.sidebar.header("Navigation")
menu = ["Campaign Management", "Customer Segmentation", "Performance Tracking", "Business Insights"]
choice = st.sidebar.radio("Go to:", menu)

if choice == "Campaign Management":
    st.header("Campaign Management 🚀")
    
    st.subheader("Create New Campaign")
    show_campaign_form()
    
    st.subheader("Existing Campaigns")
    campaigns = bm.read_campaigns()
    if campaigns:
        df = pd.DataFrame(campaigns)
        st.dataframe(df)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Update Campaign")
            campaign_to_update = st.selectbox("Select a campaign to update:", campaigns, format_func=lambda x: x['name'])
            if campaign_to_update:
                if st.button("Edit Selected Campaign"):
                    st.session_state['edit_mode'] = True
                    st.session_state['edit_campaign'] = campaign_to_update
        
        with col2:
            st.subheader("Delete Campaign")
            campaign_to_delete = st.selectbox("Select a campaign to delete:", campaigns, format_func=lambda x: x['name'])
            if campaign_to_delete:
                if st.button("Delete Selected Campaign"):
                    if bm.delete_campaign(campaign_to_delete['id']):
                        st.success(f"Campaign '{campaign_to_delete['name']}' deleted.")
                        st.rerun()
                    else:
                        st.error("Failed to delete campaign.")
    else:
        st.info("No campaigns found.")
        
    if 'edit_mode' in st.session_state and st.session_state['edit_mode']:
        st.subheader(f"Editing Campaign: {st.session_state['edit_campaign']['name']}")
        show_campaign_form(st.session_state['edit_campaign'])

elif choice == "Customer Segmentation":
    st.header("Customer Segmentation 👥")
    
    st.subheader("Manage Customers (CRUD)")
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.form("customer_form", clear_on_submit=True):
            st.markdown("##### Add a New Customer")
            name = st.text_input("Name")
            email = st.text_input("Email")
            demographics = st.text_area("Demographics (e.g., location, age)")
            submitted = st.form_submit_button("Add Customer")
            if submitted and name and email:
                if bm.create_customer(name, email, demographics):
                    st.success("Customer added successfully!")
                else:
                    st.error("Failed to add customer. Email might be a duplicate.")
                st.rerun()
                
    with col2:
        customers = bm.read_customers()
        if customers:
            st.markdown("##### All Customers")
            df_customers = pd.DataFrame(customers, columns=['ID', 'Name', 'Email', 'Demographics'])
            st.dataframe(df_customers, use_container_width=True)
    
    st.subheader("Create Dynamic Segments")
    with st.form("segment_form", clear_on_submit=True):
        segment_name = st.text_input("Segment Name")
        criteria = st.text_area("Segment Criteria (e.g., 'location = North', 'age < 30')", placeholder="This field can be used to describe the dynamic logic for your team.")
        segment_submitted = st.form_submit_button("Create Segment")
        if segment_submitted and segment_name:
            segment_id = bm.create_segment(segment_name, criteria)
            if segment_id:
                st.success(f"Segment '{segment_name}' created!")
            else:
                st.error("Failed to create segment.")
            st.rerun()
    
    st.subheader("Existing Segments")
    segments = bm.read_segments()
    if segments:
        for segment in segments:
            st.markdown(f"**Segment:** {segment['name']} (ID: {segment['id']})")
            st.markdown(f"**Criteria:** {segment['criteria']}")
            st.markdown(f"**Customers in this segment:** {', '.join([c[1] for c in segment['customers']])}")
            if st.button(f"Delete Segment {segment['name']}", key=f"delete_segment_{segment['id']}"):
                if bm.delete_segment(segment['id']):
                    st.success(f"Segment '{segment['name']}' deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete segment.")
    else:
        st.info("No segments created yet.")

elif choice == "Performance Tracking":
    st.header("Performance Tracking 📈")
    
    st.subheader("Log New Performance Data (Simulated)")
    campaigns = bm.read_campaigns()
    if campaigns:
        campaign_select = st.selectbox("Select a Campaign to log data for:", campaigns, format_func=lambda x: x['name'])
        
        with st.form("log_form"):
            emails_sent = st.number_input("Emails Sent", min_value=0)
            emails_opened = st.number_input("Emails Opened", min_value=0)
            clicks = st.number_input("Clicks", min_value=0)
            log_submitted = st.form_submit_button("Log Data")
            
            if log_submitted:
                if emails_opened > emails_sent:
                    st.warning("Emails opened cannot be more than emails sent.")
                else:
                    if bm.log_performance_metric(campaign_select['id'], emails_sent, emails_opened, clicks):
                        st.success("Performance data logged successfully!")
                    else:
                        st.error("Failed to log performance data.")
    else:
        st.warning("Please create a campaign in 'Campaign Management' first.")
    
    st.subheader("Real-Time Dashboard")
    performance_data = bm.get_performance_metrics()
    if performance_data:
        df_performance = pd.DataFrame(performance_data, columns=['ID', 'Campaign ID', 'Emails Sent', 'Emails Opened', 'Clicks', 'Timestamp'])
        
        # Display aggregated metrics for each campaign
        df_agg = df_performance.groupby('Campaign ID').agg({
            'Emails Sent': 'sum',
            'Emails Opened': 'sum',
            'Clicks': 'sum'
        }).reset_index()
        df_agg['Open Rate'] = (df_agg['Emails Opened'] / df_agg['Emails Sent'] * 100).fillna(0).round(2)
        df_agg['Click-Through Rate'] = (df_agg['Clicks'] / df_agg['Emails Opened'] * 100).fillna(0).round(2)
        
        st.markdown("##### Key Metrics by Campaign")
        st.dataframe(df_agg, use_container_width=True)
        
        st.markdown("##### Performance Data Over Time")
        st.line_chart(df_performance, x='Timestamp', y=['Emails Sent', 'Emails Opened', 'Clicks'])
    else:
        st.info("No performance data available yet.")

elif choice == "Business Insights":
    st.header("Business Insights 🧠")
    
    st.subheader("Campaign Totals and Averages")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Campaigns", bm.get_campaign_count())
    with col2:
        total_budget = bm.get_total_campaign_budget()
        st.metric("Total Campaign Budget", f"${total_budget:,.2f}")
    with col3:
        avg_clicks = bm.get_average_clicks_per_campaign()
        st.metric("Average Clicks (All Campaigns)", f"{avg_clicks:.2f}")

    st.subheader("Performance Highlights")
    max_min_metrics = bm.get_max_min_metrics()
    if max_min_metrics:
        st.markdown(f"**Highest Clicks in a single entry:** {max_min_metrics.get('max_clicks', 'N/A')}")
        st.markdown(f"**Lowest Clicks in a single entry:** {max_min_metrics.get('min_clicks', 'N/A')}")
        st.markdown(f"**Highest Emails Sent in a single entry:** {max_min_metrics.get('max_sent', 'N/A')}")
        st.markdown(f"**Highest Emails Opened in a single entry:** {max_min_metrics.get('max_opened', 'N/A')}")
    
    most_successful = bm.get_most_successful_campaign()
    if most_successful:
        st.success(f"The most successful campaign is '{most_successful[0]}' with a total of {most_successful[1]} clicks.")
    else:
        st.info("No clicks data to determine the most successful campaign.")