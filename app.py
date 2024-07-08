import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('election_results_2024.csv')

data = load_data()
data['Margin'] = pd.to_numeric(data['Margin'], errors='coerce')
data['Margin'] = data['Margin'].fillna(0)

# Title of the app
st.title('Lok Sabha Election 2024 Insights')
# constituencies = data['Constituency'].unique()
# selected_constituency = st.selectbox('Select Constituency', constituencies)
# Sidebar with options
st.sidebar.title('Choose an Analysis')
analysis_choice = st.sidebar.selectbox('Choose an analysis:',
                                       ['Number of Seats Won by Each Party',
                                        'Comparison of Votes for Candidates',
                                        'Candidates with Highest and Lowest Margin of Victory',
                                        'Histogram of Margin of Victory',
                                        'Votes Distribution by Party',
                                        'Top Trailing Parties',
                                        'Top Leading Parties'])

# Function to show number of seats won by each party
def show_seats_won():
    st.subheader('Number of Seats Won by Each Party')
    seats_won = data['Leading Party'].value_counts()
    st.write(seats_won)

    # Dropdown for party selection
    selected_party = st.selectbox('Select Party to See its Won Seats per Constituency:', [''] + list(seats_won.index))
    
    if selected_party:
        st.subheader(f'Constituencies and Seats Won by {selected_party}')
        party_data = data[data['Leading Party'] == selected_party][['Constituency', 'Margin']]
        st.table(party_data)

# Function to show comparison of votes for candidates
def show_candidate_comparison():
    st.subheader('Comparison of Votes for Candidates')

    # Constituency selection dropdown
    constituencies = data['Constituency'].unique()
    selected_constituency = st.selectbox('Select Constituency', constituencies)

    # Filter data for the selected constituency
    constituency_data = data[data['Constituency'] == selected_constituency]

    # Extract leading and trailing candidates
    leading_candidate = constituency_data.iloc[0]['Leading Candidate']
    trailing_candidate = constituency_data.iloc[0]['Trailing Candidate']
    margin = constituency_data.iloc[0]['Margin']

    # Display the data in a clear format
    st.write(f"Leading Candidate: {leading_candidate}")
    st.write(f"Trailing Candidate: {trailing_candidate}")
    st.write(f"Margin of Victory: {margin} votes")

    # Optionally, you can also show the party affiliation if needed:
    leading_party = constituency_data.iloc[0]['Leading Party']
    trailing_party = constituency_data.iloc[0]['Trailing Party']
    st.write(f"Leading Party: {leading_party}")
    st.write(f"Trailing Party: {trailing_party}")


# Function to show candidates with highest and lowest margin of victory
def show_margin_comparison():
    st.subheader('Candidates with Highest and Lowest Margin of Victory')
    highest_margin_entry = data.loc[data['Margin'].idxmax()]
    lowest_margin_entry = data.loc[data['Margin'].idxmin()]

    data_to_plot = pd.DataFrame({
        'Candidate': [highest_margin_entry['Leading Candidate'], lowest_margin_entry['Leading Candidate']],
        'Party': [highest_margin_entry['Leading Party'], lowest_margin_entry['Leading Party']],
        'Margin': [highest_margin_entry['Margin'], lowest_margin_entry['Margin']]
    })

    # Plot comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=data_to_plot, x='Candidate', y='Margin', hue='Party', palette='muted', ax=ax)
    ax.set_title('Candidates with Highest and Lowest Margin of Victory')
    ax.set_xlabel('Candidate')
    ax.set_ylabel('Margin of Victory')
    ax.tick_params(axis='x', rotation=45)

    # Display plot using st.pyplot()
    st.pyplot(fig)

# Function to show histogram of margin of victory
def show_margin_histogram():
    st.subheader('Histogram of Margin of Victory')
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Margin'], bins=20, kde=True)
    plt.title('Histogram of Margin of Victory')
    plt.xlabel('Margin of Victory')
    plt.ylabel('Frequency')
    st.pyplot()

def show_party_votes_pie():
    total_seats = 543

        # Calculate number of seats won by each leading party
    seats_won = data['Leading Party'].value_counts()

    # Calculate percentages of seats won
    party_seat_percentages = seats_won / total_seats * 100

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 10))  # Adjust size here
    wedges, texts, autotexts = ax.pie(party_seat_percentages, labels=party_seat_percentages.index, autopct='%1.1f%%', startangle=140, wedgeprops=dict(edgecolor='w'))
    ax.set_title('Seats Distribution by Party', pad=20)
    ax.axis('equal')

    # Add percentages next to each slice
    for autotext in autotexts:
        autotext.set_color('white')  # Set text color to white for better visibility

    # Legend and plot display
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='medium')

    # Show plot in Streamlit
    st.pyplot(fig)

    # Dropdown to select party and display seats won
    selected_party = st.selectbox('Select Party:', [''] + list(party_seat_percentages.index))

    if selected_party:
        st.subheader(f'Percentage of Seats Won by {selected_party}')
        percentage_seats = party_seat_percentages[selected_party]
        st.write(f"{selected_party}: {percentage_seats:.2f}%")


    


# Function to show top trailing parties by votes and seats
def show_top_trailing_parties():
    st.subheader('Top 10 Trailing Parties')
    trailing_party_votes = data.groupby('Trailing Party')['Margin'].sum().sort_values(ascending=False)
    trailing_party_seats = data['Trailing Party'].value_counts()

    plt.figure(figsize=(20, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(x=trailing_party_votes.index[:10], y=trailing_party_votes.values[:10], palette='viridis')
    plt.title('Top 10 Trailing Parties by Votes')
    plt.xlabel('Party')
    plt.ylabel('Total Votes')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    sns.barplot(x=trailing_party_seats.index[:10], y=trailing_party_seats.values[:10], palette='viridis')
    plt.title('Top 10 Trailing Parties by Seats')
    plt.xlabel('Party')
    plt.ylabel('Number of Seats')
    plt.xticks(rotation=45)

    st.pyplot()

# Function to show top leading parties by votes and seats
def show_top_leading_parties():
    st.subheader('Top 10 Leading Parties')
    leading_party_votes = data.groupby('Leading Party')['Margin'].sum().sort_values(ascending=False)
    leading_party_seats = data['Leading Party'].value_counts()

    plt.figure(figsize=(20, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(x=leading_party_votes.index[:10], y=leading_party_votes.values[:10], palette='viridis')
    plt.title('Top 10 Leading Parties by Votes')
    plt.xlabel('Party')
    plt.ylabel('Total Votes')
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    sns.barplot(x=leading_party_seats.index[:10], y=leading_party_seats.values[:10], palette='viridis')
    plt.title('Top 10 Leading Parties by Seats')
    plt.xlabel('Party')
    plt.ylabel('Number of Seats')
    plt.xticks(rotation=45)

    st.pyplot()

# Display analysis based on user selection
if analysis_choice == 'Number of Seats Won by Each Party':
    show_seats_won()
elif analysis_choice == 'Comparison of Votes for Candidates':
    show_candidate_comparison()
#elif analysis_choice == 'Candidates with Highest and Lowest Margin of Victory':
    #show_margin_comparison()
#elif analysis_choice == 'Histogram of Margin of Victory':
    #show_margin_histogram()
elif analysis_choice == 'Votes Distribution by Party':
    show_party_votes_pie()
elif analysis_choice == 'Top Trailing Parties':
    show_top_trailing_parties()
elif analysis_choice == 'Top Leading Parties':
    show_top_leading_parties()
