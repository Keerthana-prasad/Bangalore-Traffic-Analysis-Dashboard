import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure the script is run with Streamlit
if __name__ == '__main__':
    # Load the data
    try:
        data = pd.read_csv("Banglore_traffic_Dataset.csv")
        data['Date'] = pd.to_datetime(data['Date'])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Dashboard Title
    st.title('Traffic Analysis Dashboard: Bangalore')
    st.write('Blending analytical precision with creative storytelling')

    # Sidebar Filters
    st.sidebar.header('Filter Data')
    
    # Area Filter (multiselect)
    area_filter = st.sidebar.multiselect(
        'Select Area',
        data['Area Name'].unique(),
        default=data['Area Name'].unique()
    )

    # Date Range Filter (slider)
    date_slider = st.sidebar.slider(
        'Select Date Range',
        min_value=data['Date'].min().date(),
        max_value=data['Date'].max().date(),
        value=(data['Date'].min().date(), data['Date'].max().date())
    )
    
    # Traffic Volume Filter (slider)
    traffic_volume_slider = st.sidebar.slider(
        'Select Traffic Volume Range',
        min_value=int(data['Traffic Volume'].min()),
        max_value=int(data['Traffic Volume'].max()),
        value=(int(data['Traffic Volume'].min()), int(data['Traffic Volume'].max()))
    )

    # Apply Filters
    data_filtered = data[
        (data['Area Name'].isin(area_filter)) &
        (data['Date'].between(pd.to_datetime(date_slider[0]), pd.to_datetime(date_slider[1]))) &
        (data['Traffic Volume'] >= traffic_volume_slider[0]) &
        (data['Traffic Volume'] <= traffic_volume_slider[1])
    ]

    # Handle empty data
    if data_filtered.empty:
        st.warning('No data available for the selected filters.')
        st.stop()

    # KPI Section
    st.write('### Key Performance Indicators')
    st.metric('Average Traffic Volume', f"{data_filtered['Traffic Volume'].mean():,.2f}")
    st.metric('Average Speed (km/h)', f"{data_filtered['Average Speed'].mean():,.2f}")
    st.metric('Average Congestion Level (%)', f"{data_filtered['Congestion Level'].mean():,.2f}")

    # Plot 1: Traffic Volume by Area
    st.write('### Traffic Volume by Area')
    fig1 = px.bar(
        data_filtered, 
        x='Area Name', 
        y='Traffic Volume', 
        color='Congestion Level', 
        title='Traffic Volume vs Congestion Level',
        labels={'Traffic Volume': 'Traffic Volume (Units)', 'Area Name': 'Area'}
    )
    st.plotly_chart(fig1)

    # Plot 2: Speed vs. Congestion Level
    st.write('### Speed vs. Congestion Level')
    fig2 = px.scatter(
        data_filtered, 
        x='Average Speed', 
        y='Congestion Level', 
        size='Traffic Volume', 
        color='Area Name', 
        title='Speed vs Congestion Level',
        labels={'Average Speed': 'Speed (km/h)', 'Congestion Level': 'Congestion (%)'}
    )
    st.plotly_chart(fig2)

    # Plot 3: Environmental Impact (Pie Chart)
    st.write('### Environmental Impact by Area')
    fig3 = px.pie(
        data_filtered, 
        values='Environmental Impact', 
        names='Area Name', 
        title='Environmental Impact by Area'
    )
    st.plotly_chart(fig3)

    # Additional Insights
    st.write('### Insights and Recommendations')
    st.write("- Areas with consistently high congestion should explore traffic management solutions.")
    st.write("- Encourage the use of public transport in areas with poor signal compliance.")
    st.write("- Monitor environmental impact in densely populated areas for effective pollution control.")

    # Data Preview
    st.write('### Data Preview')
    st.dataframe(data_filtered)
