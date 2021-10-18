import botometer
import pandas as pd
import numpy as np
import json


# Function to open a JSON file
def read_json(filename):
    with open(filename) as f:
        json_file = f.read()
        data = json.loads(json_file)
    return data


rapidapi_key = "XXXXXXXXXX"
twitter_app_auth = {
    'consumer_key': 'XXXXXXXXXX',
    'consumer_secret': 'XXXXXXXXXX',
    'access_token': 'XXXXXXXXXX',
    'access_token_secret': 'XXXXXXXXXX',
  }


bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# reading df with users
df = pd.read_csv('users.csv')

# List with users
users = []
for user in df['username']:
    users.append(user)

# Collecting data

i = 0  # Tag
# Check a sequence of accounts
for screen_name, result in bom.check_accounts_in(users):
    with open(f'results\\user_{i}.json', 'w') as f:
        content = json.dumps(result)
        f.write(content)
    i += 1


connection_errors = []  # list to store errors connecting to the API

# Creating a new dataframe with results
# Display Score and CAP (Universal, because they are pt-br accounts)
df2 = pd.DataFrame(columns = ['username', 'display_score', 'cap'])

for i in range(237894):
    filename = f'results\\user_{i}.json'
    usr = {}  # Create a new dict to store user information
    usr = read_json(filename)

    # Adding relevant information to df2
    # username, display_score, cap
    try:
        username = usr['user']['user_data']['screen_name']
        display_score = usr['display_scores']['universal']['overall']
        cap = usr['cap']['universal']   
        
        row = {'username': username, 'display_score': display_score, 'cap': cap}
    except KeyError:
        row = {'username': df['username'][i], 'display_score':np.nan, 'cap':np.nan}  # Error in analysis of JSON file

        # Connection errors
        if 'Connection aborted' in usr['error']:
            connection_errors.append(i) 

    # Add new line
    df2 = df2.append(row, ignore_index=True)

# store results in a new df
df2.to_csv('users_cap.csv', index=False)


# check errors
if len(connection_errors) == 0:
    print('No errors detected.')
else:
    print(f'Errors detected in users: {connection_errors}')
