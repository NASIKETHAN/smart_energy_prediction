import streamlit as st
import pandas as pd

data = pd.read_csv('prediction_results_1.csv', parse_dates=['timestamp'])
user_data = pd.read_csv('user_energy_data_1.csv', parse_dates=['timestamp']) 

OVERCONSUMPTION_THRESHOLD = 0.0600  
LOW_CONSUMPTION_THRESHOLD = 0.0500  

st.title('Energy Prediction Dashboard')

st.sidebar.header("Select Date Range for Prediction Data")
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

if st.sidebar.button('Apply Date Filter'):
    if start_date and end_date:
        mask = (data['timestamp'] >= start_date) & (data['timestamp'] <= end_date)
        filtered_data = data.loc[mask]
        filtered_data['status'] = filtered_data['predicted_energy'].apply(lambda x: 
                                                                          'Overconsumption' if x > OVERCONSUMPTION_THRESHOLD 
                                                                          else ('Low Consumption' if x < LOW_CONSUMPTION_THRESHOLD 
                                                                                else 'Normal'))
    else:
        filtered_data = data.head(20)  
else:
    filtered_data = data.head(20) 
    filtered_data['status'] = filtered_data['predicted_energy'].apply(lambda x: 
                                                                      'Overconsumption' if x > OVERCONSUMPTION_THRESHOLD 
                                                                      else ('Low Consumption' if x < LOW_CONSUMPTION_THRESHOLD 
                                                                            else 'Normal'))

st.write(f"Showing results for the period from {start_date} to {end_date}:")
st.dataframe(filtered_data[['timestamp', 'predicted_energy', 'status']])

st.subheader("Predicted Energy Output Over Time")
st.write("The line chart below shows the predicted energy output (in kWh) over time for the selected date range.")

if not filtered_data.empty:
    chart_data = filtered_data.set_index('timestamp')['predicted_energy']
    
    st.line_chart(chart_data)
    
    st.write("X-Axis: Timestamp (Date and Time)")
    st.write("Y-Axis: Predicted Energy Output (kWh)")

    st.write(f"**Overconsumption Threshold**: {OVERCONSUMPTION_THRESHOLD} kWh (Values above this indicate overconsumption)")
    st.write(f"**Low Consumption Threshold**: {LOW_CONSUMPTION_THRESHOLD} kWh (Values below this indicate low consumption)")

    st.subheader("Consumption Status Alerts")
    if (filtered_data['status'] == 'Overconsumption').any():
        st.warning("Warning: Overconsumption detected during the selected period!")
    elif (filtered_data['status'] == 'Low Consumption').any():
        st.info("Info: Low consumption detected during the selected period.")
    else:
        st.success("Normal consumption during the selected period.")

st.title('Energy Usage Comparison')

comparison_start_date = st.sidebar.date_input('Start Date for Comparison')
comparison_end_date = st.sidebar.date_input('End Date for Comparison')

comparison_start_date = pd.to_datetime(comparison_start_date)
comparison_end_date = pd.to_datetime(comparison_end_date)

comparison_mask = (data['timestamp'] >= comparison_start_date) & (data['timestamp'] <= comparison_end_date)
comparison_filtered_data = data[comparison_mask]

if 'actual_energy' not in data.columns:
    comparison_filtered_data['actual_energy'] = comparison_filtered_data['predicted_energy'] * 0.95  # Example placeholder: 95% of predicted energy

st.subheader("Predicted vs Actual Energy Usage")
st.line_chart(comparison_filtered_data[['timestamp', 'predicted_energy', 'actual_energy']].set_index('timestamp'))

st.title('User Energy Consumption Dashboard')

st.subheader("Energy Consumption Overview")
st.line_chart(user_data.set_index('timestamp')['energy_consumed'])

peak_usage_time = user_data[user_data['energy_consumed'] == user_data['energy_consumed'].max()]
st.write(f"Peak Usage Time: {peak_usage_time['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').values[0]}")
st.write(f"Total Energy Consumed: {user_data['energy_consumed'].sum()} kWh")

st.write("Energy Saving Tips:")
st.write("1. Try to reduce consumption during peak hours.")
st.write("2. Switch to energy-efficient appliances.")
