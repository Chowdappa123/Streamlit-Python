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
from faker import Faker

# Enable screencast mode
st.config.screencast = True

#JMETER_PATH = os.environ['/home/pin/ApacheJmeter/apache-jmeter-5.5']
JMETER_PATH = '/home/pin/ApacheJmeter/apache-jmeter-5.5'
os.environ['JMETER_PATH'] = JMETER_PATH
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]
faker = Faker()
def generate_csv():

 with open("/home/pin/ApacheJmeter/apache-jmeter-5.5/bin/saptr1.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    data = ["firstName,lastName,emailAddress,mobilePhone"]
    for line in data:
        writer.writerow(line.split(","))
		
    start_value = 1
    start_Phone = 8249388122

    for i in range(0, 10):
        
        firstName = f"Team_{start_value + i}"
        lastName = f"PT_{start_value + i}"
        emailAddress = f"PT_Team_{start_value + i}@gmail.com"
        mobilePhone = f"{start_Phone + i}"
        data1 = [f"{firstName},{lastName},{emailAddress},{mobilePhone}"]
        for line in data1:
            writer.writerow(line.split(","))

def update_jmx():
 # Parse the JMX file
 csv_file_path = '/home/pin/ApacheJmeter/apache-jmeter-5.5/bin/saptr1.csv'
 tree = ET.parse('/home/pin/ApacheJmeter/apache-jmeter-5.5/bin/dbsignup.jmx')
 root = tree.getroot()
# Find the CSVDataSet element(s)
 for csv_dataset in root.iter('CSVDataSet'):
# Modify the filename attribute
  csv_dataset.set('filename', csv_file_path)
# Write the modified XML back to the JMX file
 tree.write('/home/pin/ApacheJmeter/apache-jmeter-5.5/bin/dbsignup.jmx')


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
    #st.write('You selected `%s`' % selected_filename + '. To execute this test plan, click on Run button as shown below.')
    report.to_file(output_file=random_filename)
    #st.markdown(report)
    return

def jmeter_execute_load():
    global JMETER_PATH
    #Changing Directory to Root
    #os.chdir('.')
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
    #jmeterfilename = jmeter_execute()
    #st.write('You selected `%s`' % jmeterfilename)

def jmeter_execute(selected_filename):
    global JMETER_PATH
    logFileName = "results_" + current_time + ".jtl"
    
    st.text('Results file is ' + logFileName)

    os.chdir(JMETER_PATH + '/bin')
    #st.text('Your curret directory is ' + os.getcwd())
    cmd = "./jmeter.sh -n -t " + selected_filename + " -l " + logFileName
    st.text('Executing ' + cmd)
    #os.chdir(".")
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
        st.markdown("<h1 style='text-align: center; color: orange; font-size: 40px;'> Recommendation</h1>", unsafe_allow_html=True)
        # Calculate the throughput recommendation
        elapsed_sum = df['elapsed'].sum()
        request_count = len(df)
        throughput = request_count / elapsed_sum * 1000
        throughput_data = df.groupby(['label'])['elapsed'].agg(['count', 'mean'])
        throughput_data['throughput'] = throughput_data['count'] / elapsed_sum * 1000
        throughput_data = throughput_data[['throughput', 'count', 'mean']].reset_index()
        average_response_time = df['elapsed'].mean()

        recommendations = []
    if average_response_time > 50:
        #st.write("since average response time is greater than the targeted")
        recommendations.append("Code Optimization.")
        recommendations.append("Change the system configuration.")
        recommendations.append("Implement load balancing techniques to distribute the incoming traffic across multiple servers.")
        recommendations.append("Using GC, kill all the unnecessary processes and free up the memory stacks.")


        recommendation = []

    if throughput < 60:
        recommendation.append("Implement Concurrent Processing.")
        recommendation.append("Implement connection pooling to reuse and manage database connections.")
        recommendation.append("Optimize Database Operations.")
        recommendation.append("Using GC, kill all the unnecessary processes and free up the memory stacks.")
    if recommendations:
        st.markdown('<span style="color: black; font-weight: bold; font-size: 20px;">Since average response time is greater than the target response time</span>', unsafe_allow_html=True)

        for index, rec in enumerate(recommendations, start=1):
            st.write(f'{index}. {rec}')
    else:
        st.write('No recommendations at this time.')

    if recommendation:
        st.markdown('<span style="color: black; font-weight: bold; font-size: 20px;">Since throughput is less than the target throughput</span>', unsafe_allow_html=True)
        for index, rec in enumerate(recommendation, start=1):
            st.write(f'{index}. {rec}')
    else:
        st.write('No recommendations at this time.')

        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)  # Retrieves the CPU usage as a percentage

        # Get memory usage
        memory = psutil.virtual_memory()
        total_memory = memory.total
        available_memory = memory.available
        memory_usage = (total_memory - available_memory) / total_memory * 100  # Calculates memory usage as a percentage

        # Print CPU and memory usage
        st.write("CPU Usage: {:.2f}%".format(cpu_usage))
        st.write("Memory Usage: {:.2f}%".format(memory_usage))

        # Add CPU and memory usage recommendation based on thresholds
        CPU_THRESHOLD = 80  # Define the recommended CPU usage threshold in percentage
        MEMORY_THRESHOLD = 70  # Define the recommended memory usage threshold in percentage
        if cpu_usage > CPU_THRESHOLD:
           st.warning("High CPU usage. Consider optimizing performance.")
        if memory_usage > MEMORY_THRESHOLD:
            st.warning("High memory usage. Consider optimizing performance.")

  
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
    #jmeter_run = st.radio('Select',('Default','Execute','Analyze'))
    #if jmeter_run == 'Execute':
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

        st.subheader('Summary Report - Response Time')
        st.write(data.groupby('label')['elapsed'].describe(percentiles=[0.75,0.95,0.99]))

        st.subheader('Error Count')
        errCount = data.groupby(['label','responseCode'])['responseCode'].count()
        st.write(errCount)

        if show_graphs:
            chart_data = pd.DataFrame(data,columns=['timeStamp','Latency','label','responseCode','elapsed','Connect','bytes'])

            st.subheader("Graph between Timestamp and Latency")
                
            st.vega_lite_chart(chart_data, {
                "mark": {"type": "bar", "color": "maroon"},    
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
                "mark": {"type": "bar", "color": "aqua"},    
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

            st.subheader("Graph between Timestamp and Response Time")
            st.vega_lite_chart(chart_data, {
                "mark": {"type": "bar", "color": "orange"},    
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

            st.subheader("Graph between Timestamp and Response Time - Line Chart")
            st.vega_lite_chart(chart_data, {
            "mark": "line",
        "encoding": {
            "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "elapsed", "type": "quantitative"}
                ],
            "x": {"field": "timeStamp", "type": "temporal"},
            "y": {"field": "elapsed", "type": "quantitative"},
            "color": {"field": "label", "type": "nominal"}
        },
                })
        
            st.subheader("Graph between Timestamp and Response Time - Bar Chart")
            st.vega_lite_chart(chart_data, {
            "mark": "bar",
        "encoding": {
            "tooltip": [
                {"field": "timeStamp", "type": "temporal"},
                {"field": "label", "type": "nominal"},
                {"field": "elapsed", "type": "quantitative"}
                ],
            "x": {"field": "timeStamp", "type": "temporal"},
            "y": {"field": "elapsed", "type": "quantitative"},
            "color": {"field": "label", "type": "nominal"}
        },
                })

            st.subheader("Histogram")
            st.vega_lite_chart(chart_data, {
                "transform": [{
                "filter": {"and": [
                {"field": "timeStamp", "valid": True},
                {"field": "elapsed", "valid": True}
                ]}
            }],
            "mark": "rect",
            "width": 300,
            "height": 200,
            "encoding": {
                "x": {
                "field": "timeStamp",
                "type": "temporal"
                },
                "y": {
                "field": "elapsed",
                "type": "quantitative"
                },
                "color": {
                "aggregate": "count",
                "type": "quantitative"
                }
            },
            "config": {
                "view": {
                "stroke": "transparent"
                }
            }
                    })

            st.subheader("Histogram")
            st.vega_lite_chart(chart_data, {
                "transform": [{
                "filter": {"and": [
                {"field": "timeStamp", "valid": True},
                {"field": "Connect", "valid": True}
                ]}
            }],
            "mark": "rect",
            "width": 300,
            "height": 200,
            "encoding": {
                "x": {
                "field": "timeStamp",
                "type": "temporal"
                },
                "y": {
                "field": "Connect",
                "type": "quantitative"
                },
                "color": {
                "aggregate": "count",
                "type": "quantitative"
                }
            },
            "config": {
                "view": {
                "stroke": "transparent"
                }
            }
                    })

            st.subheader("Scatter Plot between Timestamp and Response Time")
            st.vega_lite_chart(chart_data, {
                    
                "selection": {
                "grid": {
                "type": "interval", "bind": "scales"
                }
            },
            "mark": "circle",
            "encoding": {
                "tooltip": [
                    {"field": "timeStamp", "type": "temporal"},
                    {"field": "label", "type": "nominal"},
                    {"field": "elapsed", "type": "quantitative"}
                    ],
                "x": {
                "field": "timeStamp", "type": "temporal"    },
                "y": {
                "field": "elapsed", "type": "quantitative"    },
                "size": {"field": "label", "type": "nominal"}
            },
                    })
    if menu_sel=='Recommendations' :
        st.title('Recommendations')
        jmeter_recommend()
    if menu_sel=='Generate csv' :
        st.title('Generate csv')
        st.write("csv file is generated")
        generate_csv()
    if menu_sel=='Update jmx' :
        st.title('Update jmx')
        st.write("jmx is updated")
        update_jmx()

if __name__== "__main__":
    main()
