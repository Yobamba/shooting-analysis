import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # type: ignore

# Loading the csv file into a dataframe
raw_df = pd.read_csv("games_details.csv", low_memory=False)

# Selecting only the relevant columns
df = raw_df[['PLAYER_ID', 'PLAYER_NAME', 'START_POSITION', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT']]

# Handle any missing or incorrect data
df = df.dropna(subset=['FGM', 'FGA', 'FG_PCT'])

# Ensure numeric data types for calculations
df['FGM'] = pd.to_numeric(df['FGM'], errors='coerce')
df['FGA'] = pd.to_numeric(df['FGA'], errors='coerce')
df['FG_PCT'] = pd.to_numeric(df['FG_PCT'], errors='coerce')
df['FG3M'] = pd.to_numeric(df['FG3M'], errors='coerce')
df['FG3A'] = pd.to_numeric(df['FG3A'], errors='coerce')
df['FG3_PCT'] = pd.to_numeric(df['FG3_PCT'], errors='coerce')
df['FTM'] = pd.to_numeric(df['FTM'], errors='coerce')
df['FTA'] = pd.to_numeric(df['FTA'], errors='coerce')
df['FT_PCT'] = pd.to_numeric(df['FT_PCT'], errors='coerce')



# Aggregate data by PLAYER_ID and PLAYER_NAME
aggregated_df = df.groupby(['PLAYER_ID', 'PLAYER_NAME']).agg({
    'FGM': 'sum',
    'FGA': 'sum',
    'FG3M': 'sum',
    'FG3A': 'sum',
    'FTM': 'sum',
    'FTA': 'sum'
}).reset_index()

# Recalculate percentages based on aggregated data
aggregated_df['FG_PCT'] = aggregated_df['FGM'] / aggregated_df['FGA']
aggregated_df['FG3_PCT'] = aggregated_df['FG3M'] / aggregated_df['FG3A']
aggregated_df['FT_PCT'] = aggregated_df['FTM'] / aggregated_df['FTA']

# Handle cases where there are no attempts (avoid division by zero)
aggregated_df['FG_PCT'] = aggregated_df['FG_PCT'].fillna(0)
aggregated_df['FG3_PCT'] = aggregated_df['FG3_PCT'].fillna(0)
aggregated_df['FT_PCT'] = aggregated_df['FT_PCT'].fillna(0)

# Calculate total points scored and shooting efficiency
aggregated_df['TOTAL_POINTS'] = aggregated_df['FGM'] * 2 + aggregated_df['FG3M'] * 3 + aggregated_df['FTM']
aggregated_df['SHOOTING_EFFICIENCY'] = (aggregated_df['FG_PCT'] + aggregated_df['FG3_PCT'] + aggregated_df['FT_PCT']) / 3

# Create a score to rank players
aggregated_df['SCORE'] = aggregated_df['TOTAL_POINTS'] * aggregated_df['SHOOTING_EFFICIENCY']

# Sort the DataFrame based on the score in descending order and select the top 10 players
top_shooters = aggregated_df.sort_values(by='SCORE', ascending=False).head(10)

# Calculate missed FGA
aggregated_df['MISSED_FGA'] = aggregated_df['FGA'] - aggregated_df['FGM']

# Sort the DataFrame based on missed FGA in descending order and select the top 30 players
top_missed_fga = aggregated_df.sort_values(by='MISSED_FGA', ascending=False).head(30)

# Sort the DataFrame based on 3-point field goals made (FG3M) in descending order and select the top 10 players
top_3_point_shooters = aggregated_df.sort_values(by='FG3M', ascending=False).head(10)

# Filter players who have attempted at least 80 shots
filtered_df = aggregated_df[aggregated_df['FGA'] >= 150]

# Sort the filtered DataFrame based on the score in ascending order and select the top 30 worst shooters
worst_shooters = filtered_df.sort_values(by='SCORE', ascending=True).head(30)

# Sort the DataFrame based on field goals made (FGM) in descending order and select the top 10 players
top_fgm_players = aggregated_df.sort_values(by='FGM', ascending=False).head(10)



print("Top 10 shooters:")
print(top_shooters)
print("\nTop 10 playesr with the most field goals made:")
print(top_fgm_players)
print("\nTop 30 players with most missed FGA:")
print(top_missed_fga)
print("\nTop 10 3-point shooters:")
print(top_3_point_shooters)
print("\nBottom 3 shooters:")
print("Top 30 Worst Shooters:")
print(worst_shooters)


# Plotting the data to show the relationship between how many shots 
# players miss and how good of a shooter they are 
plt.figure(figsize=(10, 6))
plt.scatter(aggregated_df['MISSED_FGA'], aggregated_df['SCORE'], alpha=0.5)
plt.title('Shooting Score vs Total Missed Field Goals')
plt.xlabel('Total Missed Field Goals')
plt.ylabel('Shooting Score')
plt.grid(True)
plt.show()

# Plotting the data to show the relationship between how many shots 
# players miss and how bad of a shooter they are, but focusing on the lower end
plt.figure(figsize=(10, 6))
plt.scatter(worst_shooters['MISSED_FGA'], worst_shooters['SCORE'], color='red', alpha=0.5)
plt.title('Shooting Score vs Total Missed Field Goals for Worst Shooters')
plt.xlabel('Total Missed Field Goals')
plt.ylabel('Shooting Score')
plt.grid(True)
plt.show()