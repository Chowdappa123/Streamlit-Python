import string
import random
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import subprocess
import os
import uuid
import about
import ydata_profiling
import pandas_profiling
from pandas import DataFrame
import xml.etree.ElementTree as ET
import csv
import timestamp
import psutil
import re
from faker import Faker

# Enable screencast mode
st.config.screencast = True

JMETER_PATH = '/home/pin/ApacheJmeter/apache-jmeter-5.4.3'
os.environ['JMETER_PATH'] = JMETER_PATH
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]
faker = Faker()

def generate_csv(file_path, data_count=0, include_first_name=True, include_last_name=True, include_email=True, include_phone=True, include_msisdn=True, include_account=True,include_imsi=True,include_platform=True, first_name_prefix="", last_name_prefix="", phone_prefix="",msisdn_prefix="", account_prefix="", imsi_prefix="", platform_values=""):

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        field_names = []
        if include_first_name:
            field_names.append("firstName")
        if include_last_name:
            field_names.append("lastName")
        if include_email:
            field_names.append("emailAddress")
        if include_phone:
            field_names.append("mobilePhone")
        if include_msisdn:
            field_names.append("Msisdn")
        if include_account:
            field_names.append("Accountno")
        if include_imsi:
            field_names.append("Imsi")
        if include_platform:
            field_names.append("platform")


        writer.writerow(field_names)

        numeric_set = re.findall(r'\d+', first_name_prefix)
        if len(numeric_set) > 0:
            start_first_name = int(numeric_set[-1])
        else:
            start_first_name = 0

        if include_phone and phone_prefix:
            start_phone = int(phone_prefix)
        else:
            start_phone = 0

        numeric_no = re.findall(r'\d+', last_name_prefix)
        if len(numeric_no) > 0:
            start_last_name = int(numeric_no[-1])
        else:
            start_last_name = 0

        if include_msisdn and msisdn_prefix:
            start_msisdn = int(msisdn_prefix)
        else:
            start_msisdn = 0

        numeric_part = re.findall(r'\d+', account_prefix)
        if len(numeric_part) > 0:
            start_account = int(numeric_part[-1])
        else:
            start_account = 0

        if include_imsi and imsi_prefix:
            start_imsi = int(imsi_prefix)
        else:
            start_imsi = 0

        for i in range(data_count):
            row_data = []
            if include_first_name:
                first_name = start_first_name + (i * 1)
                row_data.append(f"{first_name_prefix.rstrip(''.join(numeric_set))}{first_name}")
            if include_last_name:
                last_name = start_last_name + (i * 1)
                row_data.append(f"{last_name_prefix.rstrip(''.join(numeric_no))}{last_name}")
            if include_email:
                row_data.append(f"{first_name_prefix.rstrip(''.join(numeric_set))}{last_name_prefix.rstrip(''.join(numeric_no))}_{first_name}@gmail.com")
            if include_phone:
                row_data.append(f"{start_phone + i}")
            if include_msisdn:
                row_data.append(f"{start_msisdn + i}")
            if include_account:
                account_number = start_account + (i * 2)
                row_data.append(f"{account_prefix.rstrip(''.join(numeric_part))}{account_number}")
            if include_imsi:
                row_data.append(f"{start_imsi + i}")
            if include_platform:
                if platform_values:
                    row_data.append(platform_values[i % len(platform_values)])
                else:
                    row_data.append("")

            writer.writerow(row_data)

def updatejmx():
    jmeterFileNames = []
    jmeterdataFiles = []
    os.chdir(JMETER_PATH + '/bin')
    filenames = os.listdir(".")

    # Find JMeter test files
    for f in filenames:
        if f.endswith('.jmx'):
            jmeterFileNames.append(f)
        elif f.endswith('.csv'):
            jmeterdataFiles.append(f)

    if not jmeterFileNames:
        st.write("No JMX files found.")
        return None, None

    if not jmeterdataFiles:
        st.write("No test data files found.")
        return None, None

    selected_Jmxfile = st.selectbox('Select a JMX file', jmeterFileNames)
    selected_datafile = st.selectbox('Select a test data file', jmeterdataFiles)

    jmx_file_path = os.path.join(JMETER_PATH, 'bin', selected_Jmxfile)
    data_file_path = os.path.join(JMETER_PATH, 'bin', selected_datafile)

    return jmx_file_path, data_file_path

def update_jmx(jmx_file_path, data_file_path):
    # Read the JMX file
    with open(jmx_file_path, 'r') as jmx_file:
        jmx_content = jmx_file.read()

    # Modify the JMX content to include the data file path
    updated_jmx_content = jmx_content.replace('path_to_data_file', data_file_path)

    # Save the updated JMX file
    with open(jmx_file_path, 'w') as updated_jmx_file:
        updated_jmx_file.write(updated_jmx_content)

    st.write("JMX file updated successfully!")


def main_about():
    st.title('About')
    st.markdown('---')
    #Display About section
    

def pd_profile(filename):
    df = pd.read_csv(JMETER_PATH + '/bin/' + filename)
    report = pandas_profiling.ProfileReport(df)
    #st.write(pandas_profiling.__version__)
    random_filename = ''.join("report_" + current_time) 
    random_filename = random_filename + ".html"
    st.write('Report file name is `%s`' % random_filename + ' . Report is located at ' + JMETER_PATH + '/bin/')
    report.to_file(output_file=random_filename)
    return

def jmeter_execute_load():
    global JMETER_PATH
    #Changing Directory to Root
    os.chdir(JMETER_PATH + '/bin')
    jmeterFileNames = []
    
    # Find only JMeter test plans
    for f in os.listdir("."):
        if f.endswith('.jmx'):
            jmeterFileNames.append(f)
    selected_filename = st.selectbox('Select a file to execute',jmeterFileNames)
    st.write('You selected `%s`' % selected_filename + '. To execute this test plan, click on Run button as shown below.')
    st.info('JMeter Path is ' + JMETER_PATH)
    if st.button('Run'):
        st.info('Execution has been started, you can monitor the stats in the command prompt.')
        jmeter_execute(selected_filename)
   
def jmeter_execute(selected_filename):
    global JMETER_PATH
    
    logFileName = "results_" + current_time + ".jtl"
    FileName = "htmlreports_" + current_time + ".htm"

    st.text('Results file is ' + logFileName)

    os.chdir(JMETER_PATH + '/bin')
    cmd = "./jmeter.sh -n -t " + selected_filename + " -l " + logFileName + " -e -o " + FileName 
    st.text('Executing ' + cmd)
    returned_value = os.system(cmd)

    # perform analysis on file_path
    pass

def jmeter_analyze():
    jmeterResults = []
    os.chdir(JMETER_PATH + '/bin')
    filenames = os.listdir(".")

    # Find only JMeter test results
    for f in os.listdir("."):
        if f.endswith('.jtl'):
            jmeterResults.append(f)
    selected_filename = st.selectbox('Select a file to analyze (supports only jtl extension)', jmeterResults)
    return os.path.join(selected_filename)

def jmeter_recommend():
    jmeterResults = []
    os.chdir(JMETER_PATH + '/bin')
    filenames = os.listdir(".")

    # Find only JMeter test results
    for f in os.listdir("."):
        if f.endswith('.jtl'):
            jmeterResults.append(f)
    selected_file = st.selectbox('Select a file to recommend (supports only jtl extension)', jmeterResults)
    #return os.path.join(selected_file)
    if selected_file is not None:
        # Load the CSV into a pandas dataframe
        csv_path = os.path.join(JMETER_PATH + '/bin', selected_file)
        df = pd.read_csv(csv_path)
        st.markdown("<h1 style='text-align: center; color: orange; font-size: 40px;'>Recommendation</h1>", unsafe_allow_html=True)
        elapsed_sum = df['elapsed'].sum()
        request_count = len(df)
        throughput_data = df.groupby(['label'])['elapsed'].agg(['count', 'mean'])
        throughput_data['throughput'] = throughput_data['count'] / elapsed_sum * 1000
        throughput_data = throughput_data[['throughput', 'count', 'mean']].reset_index()
        average_response_time = df['elapsed'].mean()
        failed_count = df['success'].value_counts().get(False, 0)
        error_rate = failed_count / request_count
       
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)  # Retrieves the CPU usage as a percentage

        # Get memory usage
        memory = psutil.virtual_memory()
        total_memory = memory.total
        available_memory = memory.available
        memory_usage = (total_memory - available_memory) / total_memory * 100  # Calculates memory usage as a percentage

        recommendations = []

    # Check for high response times
    max_response_time = average_response_time.max()
    #st.write(f"As the max response time = {max_response_time}")
    st.write("As the max response time = {:.2f}".format(max_response_time))
    if max_response_time <= 1000:
        recommendations.append("Response time is optimal.")

    elif max_response_time <= 3000:
        recommendations.append("Consider optimizing resource utilization for better response time.")

    elif max_response_time <= 5000:
        recommendations.append(f"Identify and optimize slow database queries.")

    else:
        recommendations.append("Significantly high response time detected . Investigate and optimize the system.")


    # Check for high error rates
    Error_per = error_rate * 100
    st.write("As the Error: {:.2f}%".format(Error_per))
    if error_rate > 0.05:
        recommendations.append("Investigate high error rate")
        if error_rate > 0.1:
            recommendations.append("Implement error handling and retry mechanisms.")

    else:
        recommendations.append("Error rate is within acceptable limits.")
        
        
     # Check for low throughput
    avg_throughput = throughput_data['throughput'].mean()
    #st.write(f"As the avg throughput = {avg_throughput}")
    st.write("As the Avg Throughput = {:.2f}".format(avg_throughput))
    if avg_throughput < 100:
        recommendations.append("Improve throughput")
    else:
        recommendations.append("Improve throughput for better performance.")

        # Additional recommendations based on throughput
        if avg_throughput < 50:
            recommendations.append("Consider increasing server capacity or optimizing test configuration.")
    
    if len(df) > 1000:
        recommendations.append("Large test, consider distributing load")

    if df['success'].mean() < 0.95:
        recommendations.append("Improve success rate")

    # CPU Usage 
    #st.write("CPU Usage: {:.2f}%".format(cpu_usage))
    if cpu_usage > 80:
        recommendations.append("High CPU usage. Consider optimizing performance.")
   
    # Memory usage
   # st.write("Memory Usage: {:.2f}%".format(memory_usage))
    if memory_usage > 70:
        recommendations.append("High memory usage. Consider optimizing performance.")

    if recommendations:
        st.markdown('<span style="color: black; font-weight: bold; font-size: 20px;">Some of the recommendations for better performance</span>', unsafe_allow_html=True)

        for index, rec in enumerate(recommendations, start=1):
            st.write(f'{index}. {rec}')
    else:
        st.write('No recommendations at this time.')
            
def main():
    menu_list = ['Generate csv','Update jmx','Execute JMeter Test Plan','Analyze JMeter Test Results', 'Recommendations','Home']

    # Display options in Sidebar
    st.sidebar.title('Navigation')
    menu_sel = st.sidebar.radio('', menu_list, index=2, key=None)

    # Display text in Sidebar
    about.display_sidebar()

    # Selecting About Menu
    if menu_sel == 'Home':
        about.display_about()

    # Selecting Execute Menu
    if menu_sel == 'Execute JMeter Test Plan':
        st.title('Execute JMeter Test Plan')
        jmeter_execute_load()


    #if jmeter_run == 'Analyze':
    if menu_sel == 'Analyze JMeter Test Results':
        st.title('Analyze JMeter Test Results')

        filename = jmeter_analyze()
        st.write('You selected `%s`' % filename)
        DATA_URL = filename

        
        st.markdown('')
        # Show Graphs Checkbox
        show_graphs = st.checkbox('Show Graphs')

        # Show Profiling Report
        profile_report = st.button('Generate Profiling Report')
       
        # Generate Profiling Report

        if profile_report:
            st.write('Generating Report for ', filename)
            pd_profile(filename)


        st.title('Apache JMeter Load Test Results')
        data = pd.read_csv(DATA_URL)
        
        #Display Start Time
        startTime = data['timeStamp'].iloc[0]/1000
        startTime = datetime.datetime.fromtimestamp(startTime).strftime('%Y-%m-%d %H:%M:%S')
        st.write('Start Time ', startTime)

        endTime = data['timeStamp'].iloc[-1]/1000
        endTime = datetime.datetime.fromtimestamp(endTime).strftime('%Y-%m-%d %H:%M:%S')
        st.write('End Time ', endTime)

        FMT = '%Y-%m-%d %H:%M:%S'
        delta = datetime.datetime.strptime(endTime, FMT) - datetime.datetime.strptime(startTime, FMT)

        st.write('Total duration of the test (HH:MM:SS) is ', delta)

        st.subheader('Summary Report')
        #st.write(data.groupby('label')['elapsed'].describe(percentiles=[0.75,0.95,0.99]))
        #st.write(data.groupby('label')['elapsed'].describe())

        summary_stats = data.groupby('label').agg({
            'label': 'count',
            'success': lambda x: (1 - (x.sum() / len(x))) * 100,
            'elapsed': ['mean', 'min', 'max', 'median', lambda x: np.percentile(x, 90), lambda x: np.percentile(x, 95),
                    lambda x: np.percentile(x, 99)]
        })
        summary_stats.columns = ['Count', 'Error%', 'Average', 'Minimum', 'Maximum', 'Median', '90th Percentile', '95th Percentile',
                             '99th Percentile']
        summary_stats.reset_index(inplace=True)

        # Calculate Transaction per Second (TPS)
        test_duration = data['timeStamp'].max() - data['timeStamp'].min()
        summary_stats['Transaction per Second (TPS)'] = summary_stats['Count'] / (test_duration / 1000)

        # Display summary statistics
        #st.write("Summary Statistics:")
        st.table(summary_stats.style.set_caption(""))

        st.subheader('Error Count')
        errCount = data.groupby(['label','responseCode'])['responseCode'].count().reset_index(name='count')
        st.write(errCount)

        if show_graphs:

            # Column selection
            columns = data.columns.tolist()
            selected_columns = st.multiselect("Select columns for analysis", columns)

            if selected_columns:
                # Display selected columns
                st.write("Selected Columns:")
                st.write(data[selected_columns])

                # Line chart
                st.write("Line Chart:")
                st.line_chart(data[selected_columns])

                # Bar
                st.write("Bar")
                st.bar_chart(data[selected_columns])

            else:
                st.warning("Please select at least one column for analysis.")

            chart_data = pd.DataFrame(data,columns=['timeStamp','Latency','label','responseCode','elapsed','Connect','bytes', 'Transaction per Second (TPS)'])

            st.subheader("Latency Graph")
                
            st.vega_lite_chart(chart_data, {
                "layer": [
                    {"mark": {"type": "point", "color": "orange"}},
                    {"mark": {"type": "line", "color": "orange"}}
                ],  
                "selection": {
                    "grid": {
                    "type": "interval", "bind": "scales"
                    }
                }, 
                'encoding': {
                    "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "Latency", "type": "quantitative"}
                ],
                'x': {'field': 'timeStamp', 'type': 'temporal'},
                'y': {'field': 'Latency', 'type': 'quantitative'},
                },
                })

            st.subheader("Graph between Timestamp and Response Code")
            st.vega_lite_chart(chart_data, {
                "mark": {"type": "line", "color": "aqua"},    
                "selection": {
                    "grid": {
                    "type": "interval", "bind": "scales"
                    }
                }, 
                'encoding': {
                    "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "responseCode", "type": "quantitative"}
                ],
                'x': {'field': 'timeStamp', 'type': 'temporal'},
                'y': {'field': 'responseCode', 'type': 'quantitative'},
                },
                })

            st.subheader(" Response Time Graph")
            st.vega_lite_chart(chart_data, {
                "layer": [
                    {"mark": {"type": "point", "color": "orange"}},
                    {"mark": {"type": "line", "color": "orange"}}
                ],
                #"mark": {"type": "bar", "color": "orange"},    
                "selection": {
                    "grid": {
                    "type": "interval", "bind": "scales"
                    }
                }, 
                'encoding': {
                    "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "elapsed", "type": "quantitative"}
                ],
                'x': {'field': 'timeStamp', 'type': 'temporal'},
                'y': {'field': 'elapsed', 'type': 'quantitative'},
                },
                })
  
            #st.subheader("Transaction per second Graph")
            #st.vega_lite_chart(chart_data, {
             #   "mark": {"type": "line", "color": "orange"},
              #  "selection": {
               #     "grid": {
                #        "type": "interval",
                 #       "bind": "scales"
                  #  }
               # },
               # "encoding": {
                #    "tooltip": [
                 #       {"field": "timeStamp", "type": "temporal"},
                  #      {"field": "label", "type": "nominal"},
                        #{"field": "elapsed", "type": "quantitative"},
                   #     {"field": "transactions", "type": "quantitative"}
                   # ],
                   # "x": {"field": "timeStamp", "type": "temporal"},
                   # "y": 
                       # {"field": "elapsed", "type": "quantitative", "title": "Elapsed Time"},
                    #     {"field": "Transaction per Second (TPS)", "type": "quantitative", "title": "Transactions Per Second"}
                    
               # }
           # })

            st.subheader("Graph between Timestamp and Connect Time")
            st.vega_lite_chart(chart_data, {
                "mark": {"type": "bar", "color": "darkgreen"},    
                "selection": {
                    "grid": {
                    "type": "interval", "bind": "scales"
                    }
                }, 
                'encoding': {
                    "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "Connect", "type": "quantitative"}
                ],
                'x': {'field': 'timeStamp', 'type': 'temporal'},
                'y': {'field': 'Connect', 'type': 'quantitative'},
                },
                })

            st.subheader("Graph between Timestamp and bytes")
            st.vega_lite_chart(chart_data, {
                "mark": {"type": "bar", "color": "darkblue"},    
                "selection": {
                    "grid": {
                    "type": "interval", "bind": "scales"
                    }
                }, 
                'encoding': {
                    "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "bytes", "type": "quantitative"}
                ],
                'x': {'field': 'timeStamp', 'type': 'temporal'},
                'y': {'field': 'bytes', 'type': 'quantitative'},
                },
                })

      

    if menu_sel=='Recommendations' :
        st.title('Recommendations')
        jmeter_recommend()

    if menu_sel=='Generate csv' :
        st.title('Generate CSV')
        data_count = st.number_input("Enter the number of data entries", min_value=0, step=1)
        file_name = st.text_input("Enter the file name with .csv extension", value="")
        file_path = f"/home/pin/ApacheJmeter/apache-jmeter-5.4.3/bin/{file_name}"

        include_first_name = st.checkbox("first name", value=False)
        if include_first_name:
            first_name_prefix = st.text_input("Enter the first name prefix", value="")
        else:
            first_name_prefix = ""

        include_last_name = st.checkbox("last name", value=False)
        if include_last_name:
            last_name_prefix = st.text_input("Enter the last name prefix", value="")
        else:
            last_name_prefix = ""

        include_email = st.checkbox("email", value=False)
        include_phone = st.checkbox("phone", value=False)
        if include_phone:
            phone_prefix = st.text_input("Enter the phone prefix", value="")
        else:
            phone_prefix = ""
        include_msisdn = st.checkbox("Msisdn", value=False)
        if include_msisdn:
            msisdn_prefix = st.text_input("Enter the msisdn prefix", value="")
        else:
            msisdn_prefix = ""
        include_account = st.checkbox("Accountno", value=False)
        if include_account:
            account_prefix = st.text_input("Enter the account prefix", value="")
        else:
            account_prefix = ""
        
        include_imsi = st.checkbox("Imsi", value=False)
        if include_imsi:
            imsi_prefix = st.text_input("Enter the imsi prefix", value="")
        else:
            imsi_prefix = ""

        include_platform = st.checkbox("Platform", value=False)
        if include_platform:
            platform_values = st.multiselect("Select platform options", ["Prepaid", "Postpaid"], default=[])
        else:
            platform_values = []

        if st.button("Generate CSV"):
            generate_csv(
                file_path,
                int(data_count),
                include_first_name,
                include_last_name,
                include_email,
                include_phone,
                include_msisdn,
                include_account,
                include_imsi,
                include_platform,
                first_name_prefix,
                last_name_prefix,
                phone_prefix,
                msisdn_prefix,
                account_prefix,
                imsi_prefix,
                platform_values
            )
            st.success("CSV generated successfully!")


    if menu_sel=='Update jmx' :
        st.title('Update JMX')
        jmx_file_path, data_file_path = updatejmx()

        if jmx_file_path and data_file_path:
        #st.write("Selected JMX file:", jmx_file_path)
        #st.write("Selected test data file:", data_file_path)

           if st.button("Update JMX with Data File"):
               update_jmx(jmx_file_path, data_file_path)

   

if __name__== "__main__":
    main()
