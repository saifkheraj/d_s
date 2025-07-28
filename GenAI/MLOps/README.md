# Automated Feature Engineering with FeatureTools: NHL Dataset Example

## Overview

This README explains automated feature engineering using the FeatureTools library on a Kaggle NHL (National Hockey League) dataset. The goal is to predict if a game is a "regular season" or "postseason" (playoff) game based on summaries of play events (e.g., shots, goals, penalties). FeatureTools automates creating features by aggregating detailed "play" events into game-level summaries.

Key concepts:
- **Parent DataFrame**: `games_df` - One row per game (basic game info like type: 'R' for regular, 'P' for postseason).
- **Child DataFrame**: `plays_df` - Many rows per game (detailed events like goals or shots, linked by `game_id`).
 
We'll use Python libraries: Pandas, FeatureTools, Framequery, and scikit-learn. This automates what would otherwise be manual work.

## Prerequisites

- Python 3.7+ installed.
- Install libraries:
  ```
  pip install pandas featuretools framequery scikit-learn
  ```
- Download the NHL dataset from Kaggle (requires a Kaggle account and API key):
  - Place your `kaggle.json` in `~/.kaggle/`.
  - Run: `kaggle datasets download -d martinellis/nhl-game-data` (or similar; check Kaggle for exact name).
  - Unzip to get CSVs like `game.csv` (for games) and `game_plays.csv` (for plays).

## Step-by-Step Guide

### Step 1: Load and Prepare Datasets

Load the CSV files into Pandas DataFrames. Clean the plays DataFrame by dropping unnecessary columns and filling missing values with 0.

**Code Snippet:**
```python
import pandas as pd

# Load datasets (adjust paths as needed)
games_df = pd.read_csv('path/to/game.csv')  # Parent: One row per game
plays_df = pd.read_csv('path/to/game_plays.csv')  # Child: Many rows per game

# Clean plays_df
columns_to_drop = ['dateTime', 'rink_side', 'secondaryType']  # Example columns to drop; adjust based on your data
plays_df = plays_df.drop(columns=columns_to_drop, errors='ignore')
plays_df = plays_df.fillna(0)

print(games_df.head())  # View parent sample
print(plays_df.head())  # View child sample
```

**Example Parent Records (games_df - Sample 5 Rows):**

| game_id    | season  | type | date_time            | away_team_id | home_team_id | away_goals | home_goals | outcome      | home_rink_side_start | venue              | venue_link         | venue_time_zone_id | venue_time_zone_offset | venue_time_zone_tz |
|------------|---------|------|----------------------|--------------|--------------|------------|------------|--------------|----------------------|--------------------|--------------------|--------------------|------------------------|--------------------|
| 2012030221 | 20122013 | P   | 2013-05-16T00:00:00Z | 3            | 6            | 2          | 3          | home win OT | left                | TD Garden         | /api/v1/venues/null | America/New_York  | -4                     | EDT                |
| 2012030222 | 20122013 | P   | 2013-05-19T00:00:00Z | 3            | 6            | 2          | 5          | home win REG| left                | TD Garden         | /api/v1/venues/null | America/New_York  | -4                     | EDT                |
| 2012030223 | 20122013 | P   | 2013-05-21T00:00:00Z | 6            | 3            | 2          | 1          | away win REG| right               | Madison Square Garden | /api/v1/venues/null | America/New_York  | -4                     | EDT                |
| 2012030224 | 20122013 | P   | 2013-05-23T00:00:00Z | 6            | 3            | 3          | 4          | home win OT | right               | Madison Square Garden | /api/v1/venues/null | America/New_York  | -4                     | EDT                |
| 2012030225 | 20122013 | P   | 2013-05-25T00:00:00Z | 3            | 6            | 1          | 3          | home win REG| left                | TD Garden         | /api/v1/venues/null | America/New_York  | -4                     | EDT                |

**Example Child Records (plays_df - Sample 5 Rows, after cleaning):**

| play_id       | game_id    | play_num | team_id_for | team_id_against | event  | x   | y   | period | periodTime | periodTimeRemaining | goals_away | goals_home | description                  | st_x | st_y |
|---------------|------------|----------|-------------|-----------------|--------|-----|-----|--------|------------|---------------------|------------|------------|------------------------------|------|------|
| 2012030221_1  | 2012030221 | 1       | NaN        | NaN            | Period Ready | 0.0 | 0.0 | 1     | 0         | 1200               | 0         | 0         | Period Ready                 | 0.0 | 0.0 |
| 2012030221_2  | 2012030221 | 2       | NaN        | NaN            | Period Start | 0.0 | 0.0 | 1     | 0         | 1200               | 0         | 0         | Period Start                 | 0.0 | 0.0 |
| 2012030221_3  | 2012030221 | 3       | NaN        | NaN            | Game Official| 0.0 | 0.0 | 1     | 0         | 1200               | 0         | 0         | Game Official                | 0.0 | 0.0 |
| 2012030221_4  | 2012030221 | 4       | 6.0        | 3.0            | Faceoff    | 0.0 | 0.0 | 1     | 0         | 1200               | 0         | 0         | Brad Marchand faceoff won against Derick Brassard | 0.0 | 0.0 |
| 2012030221_5  | 2012030221 | 5       | 6.0        | NaN            | Giveaway   | 89.0| -22.0| 1     | 16        | 1184               | 0         | 0         | Giveaway by Nathan Horton    | -89.0| 22.0|

### Step 2: Encode Categorical Features

Convert text columns in `plays_df` (e.g., 'event' like "Goal", "Shot") to numeric (one-hot encoding) using FeatureTools.

**Code Snippet:**
```python
import featuretools as ft

# Create EntitySet
es = ft.EntitySet(id='nhl_data')

# Add plays_df as entity, specify categorical columns
variable_types = {
    'event': ft.variable_types.Categorical,
    'description': ft.variable_types.Text  # If needed; adjust
}
es = es.add_dataframe(dataframe_name='plays', dataframe=plays_df, index='play_id', variable_types=variable_types)

# Encode categorical features
features_to_encode = ['event']  # Add more if needed
encoded_plays_df, feature_defs = ft.encode_categorical(es['plays'], features_to_encode)

print(encoded_plays_df.head())  # Now has dummy columns like 'event_Goal'
```

### Step 3: Aggregate Plays into Game Summaries (Deep Feature Synthesis)

Define relationships (plays as child of games) and auto-generate features (e.g., SUM of shots, COUNT of goals per game).

**Code Snippet:**
```python
# Recreate EntitySet with encoded data
es = ft.EntitySet(id='nhl_data')
es = es.add_dataframe(dataframe_name='plays', dataframe=encoded_plays_df, index='play_id')

# Normalize to create 'games' parent entity
es = es.normalize_dataframe(base_dataframe_name='plays', new_dataframe_name='games', index='game_id')

# Deep Feature Synthesis
feature_matrix, feature_defs = ft.dfs(entityset=es, target_dataframe_name='games',
                                      agg_primitives=['sum', 'max', 'min', 'count', 'mean'],
                                      trans_primitives=['add_numeric', 'subtract_numeric'])

print(feature_matrix.head())  # One row per game, with 200+ auto-generated features
print(feature_matrix.shape)   # e.g., (number_of_games, 212)
```

### Step 4: Join Features with Labels

Combine generated features with `games_df` and create a binary label (1 for postseason).

**Code Snippet:**
```python
import framequery as fq

# Make games_df available for SQL query
fq.scope(games=games_df, features=feature_matrix.reset_index())

# SQL join to add label
final_df = fq.execute("""
    SELECT 
        f.*,
        CASE WHEN g.type = 'P' THEN 1 ELSE 0 END AS label
    FROM features AS f
    JOIN games AS g ON f.game_id = g.game_id
""")

print(final_df.head())
```

### Step 5: Build and Evaluate Logistic Regression Model

Train a model to predict the label using scikit-learn.

**Code Snippet:**
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

# Prepare data (drop ID to avoid overfitting)
X = final_df.drop(columns=['game_id', 'label'])
y = final_df['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression(max_iter=1000)  # Increase iterations if needed
model.fit(X_train, y_train)

# Predict and evaluate
preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]
accuracy = accuracy_score(y_test, preds)
roc = roc_auc_score(y_test, probs)

print(f"Accuracy: {accuracy:.3f}")  # e.g., 0.947
print(f"ROC-AUC: {roc:.3f}")       # e.g., 0.923
```

## Results

The model typically achieves ~95% accuracy. You can improve it by tuning or adding more primitives in DFS.

## Running the Full Notebook

Download `FeatureEngineering.ipynb` from the tutorial and run it in Jupyter. It includes all steps.

## License

This is for educational purposes. Dataset from Kaggle (check their terms). Code is open for use.
