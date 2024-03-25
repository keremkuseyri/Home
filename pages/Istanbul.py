import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout='wide')

tab1, tab2 = st.tabs(["Quantity", "Teu"])


data= {
    ('2024-01-01', '2024-01-31'): {
        'data_count': {
            'istanbul': {'A': {'I': 58, 'E': 308, 'T': 0}, 'B': {'I': 80, 'E': 125, 'T': 14}, 'FRW': {'I': 1, 'E': 1, 'T': 0}},
            'mersin': {'A': {'I': 6, 'E': 94, 'T': 0}, 'B': {'I': 0, 'E': 9, 'T': 0}, 'FRW': {'I': 0, 'E': 0, 'T': 0}},
            'izmir': {'A': {'I': 15, 'E': 93, 'T': 0}, 'B': {'I': 24, 'E': 17, 'T': 1}, 'FRW': {'I': 4, 'E': 0, 'T': 0}}
        },
        'teu': {
            'istanbul': {'A': {'I': 192.0, 'E': 544.0996154675138, 'T': 0}, 'B': {'I': 167.0, 'E': 256.16085080329856, 'T': 19.999999999999996}, 'FRW': {'I': 2.0, 'E': 2.0, 'T': 0}},
            'mersin': {'A': {'I': 10.0, 'E': 332.0, 'T': 0}, 'B': {'I': 0, 'E': 12.0, 'T': 0}, 'FRW': {'I': 0, 'E': 0, 'T': 0}},
            'izmir': {'A': {'I': 14.0, 'E': 200.0, 'T': 0}, 'B': {'I': 42.0, 'E': 28.0, 'T': 2.0}, 'FRW': {'I': 7.0, 'E': 0, 'T': 0}}
        }
    },
    ('2024-02-01', '2024-02-29'): {
        'data_count': {
            'istanbul': {'A': {'I': 34, 'E': 264, 'T': 0}, 'B': {'I': 52, 'E': 136, 'T': 16}, 'FRW': {'I': 1, 'E': 0, 'T': 0}},
            'mersin': {'A': {'I': 8, 'E': 102, 'T': 0}, 'B': {'I': 0, 'E': 7, 'T': 0}, 'FRW': {'I': 0, 'E': 0, 'T': 0}},
            'izmir': {'A': {'I': 12, 'E': 89, 'T': 0}, 'B': {'I': 21, 'E': 21, 'T': 0}, 'FRW': {'I': 3, 'E': 1, 'T': 0}}
        },
        'teu': {
            'istanbul': {'A': {'I': 68.0, 'E': 461.8376537753159, 'T': 0}, 'B': {'I': 95.0, 'E': 260.5190668969966, 'T': 32.0}, 'FRW': {'I': 4.0, 'E': 0, 'T': 0}},
            'mersin': {'A': {'I': 33.0, 'E': 331.0, 'T': 0}, 'B': {'I': 0, 'E': 12.0, 'T': 0}, 'FRW': {'I': 0, 'E': 0, 'T': 0}},
            'izmir': {'A': {'I': 14.0, 'E': 177.0, 'T': 0}, 'B': {'I': 37.0, 'E': 33.0, 'T': 0}, 'FRW': {'I': 5.0, 'E': 4.0, 'T': 0}}
        }
    }
}


with tab1:
    table_data = []  
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'data_count': 
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"A:{city_values['A']['E']} B:{city_values['B']['E']} FRW:{city_values['FRW']['E']}",
                                'Import': f"A:{city_values['A']['I']} B:{city_values['B']['I']} FRW:{city_values['FRW']['I']}",
                                'Cross Trade': f"A:{city_values['A']['T']} B:{city_values['B']['T']} FRW:{city_values['FRW']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("Quantity")
    st.write(city_df)
                            
    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'data_count':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['A']['E']}",
                                'Import': f"{city_values['A']['I']}",
                                'Cross Trade': f"{city_values['A']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("A:")
    st.write(city_df)

    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'data_count':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['B']['E']}",
                                'Import': f"{city_values['B']['I']}",
                                'Cross Trade': f"{city_values['B']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("B:")
    st.write(city_df)                        

    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'data_count':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['FRW']['E']}",
                                'Import': f"{city_values['FRW']['I']}",
                                'Cross Trade': f"{city_values['FRW']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("FRW:")
    st.write(city_df)

    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'data_count':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['A']['E'] + city_values['B']['E'] + city_values['FRW']['E']}",
                                'Import': f"{city_values['A']['I'] + city_values['B']['I'] + city_values['FRW']['I']}",
                                'Cross Trade': f"{city_values['A']['T'] + city_values['B']['T'] + city_values['FRW']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("SUM:")
    st.write(city_df)

    fig = go.Figure()

# Add bar chart trace
    fig.add_trace(go.Bar(
        x=city_df['From Date'],
        y=city_df['Export'],
        name='Export'
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Export"
    )

    # Display the plot
    st.plotly_chart(fig)

    fig = go.Figure()

# Add bar chart trace
    fig.add_trace(go.Bar(
        x=city_df['From Date'],
        y=city_df['Import'],
        name='Import'
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Import"
    )

    # Display the plot
    st.plotly_chart(fig)

    fig = go.Figure()

# Add bar chart trace
    fig.add_trace(go.Bar(
        x=city_df['From Date'],
        y=city_df['Cross Trade'],
        name='Cross Trade'
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Cross Trade"
    )

    # Display the plot
    st.plotly_chart(fig)    

with tab2:
    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'teu':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"A:{city_values['A']['E']} B:{city_values['B']['E']} FRW:{city_values['FRW']['E']}",
                                'Import': f"A:{city_values['A']['I']} B:{city_values['B']['I']} FRW:{city_values['FRW']['I']}",
                                'Cross Trade': f"A:{city_values['A']['T']} B:{city_values['B']['T']} FRW:{city_values['FRW']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("Teu")
    st.write(city_df)


    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'teu':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['A']['E']}",
                                'Import': f"{city_values['A']['I']}",
                                'Cross Trade': f"{city_values['A']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("A:")
    st.write(city_df)

    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'teu':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['B']['E']}",
                                'Import': f"{city_values['B']['I']}",
                                'Cross Trade': f"{city_values['B']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("B:")
    st.write(city_df)                        

    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'teu':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['FRW']['E']}",
                                'Import': f"{city_values['FRW']['I']}",
                                'Cross Trade': f"{city_values['FRW']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("FRW:")
    st.write(city_df)

    table_data = [] 
    for date_range, date_data in data.items():
        for data_type, city_data in date_data.items():
            for city, city_values in city_data.items():
                if city == 'istanbul':
                    if data_type == 'teu':      
                            row = {
                                'From Date': date_range[0],
                                'To Date': date_range[1],
                                'Export': f"{city_values['A']['E'] + city_values['B']['E'] + city_values['FRW']['E']}",
                                'Import': f"{city_values['A']['I'] + city_values['B']['I'] + city_values['FRW']['I']}",
                                'Cross Trade': f"{city_values['A']['T'] + city_values['B']['T'] + city_values['FRW']['T']}"
                            }
                            table_data.append(row)
    city_df = pd.DataFrame(table_data)
    st.header("SUM:")
    st.write(city_df)

    fig = go.Figure()

# Add bar chart trace
    fig.add_trace(go.Bar(
        x=city_df['From Date'],
        y=city_df['Export'],
        name='Export'
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Export"
    )

    # Display the plot
    st.plotly_chart(fig)

    fig = go.Figure()

# Add bar chart trace
    fig.add_trace(go.Bar(
        x=city_df['From Date'],
        y=city_df['Import'],
        name='Import'
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Import"
    )

    # Display the plot
    st.plotly_chart(fig)

    fig = go.Figure()

# Add bar chart trace
    fig.add_trace(go.Bar(
        x=city_df['From Date'],
        y=city_df['Cross Trade'],
        name='Cross Trade'
    ))

    # Update layout
    fig.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Cross Trade"
    )

    # Display the plot
    st.plotly_chart(fig) 
