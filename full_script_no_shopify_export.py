import pandas as pd

############################################################################################################
# CREATING AND ORGANIZING THE DATAFRAME BELOW :
############################################################################################################
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
loop1 = 0
file_path = input('Please enter the file path for the Shopify Export Data.\n'
                  'Sample file path: /Users/adreannalaporte/Desktop/ISE 495B/data export mult events & prefs.csv\n'
                  'File path: ')
while loop1 == 0:
    if isinstance(file_path, str) and '/' in file_path and '.csv' in file_path:
        loop1 = 1
    else:
        print('Please enter a valid file path. Make sure your formatting is correct (follow sample file path given '
              'above):')
        file_path = input('File path: ')
        loop1 = 0
data = pd.read_csv(file_path)

df_participants = data
# sorting by age and then by preference
df_participants = df_participants.sort_values('Age')
df_participants = df_participants.sort_values('Preference', ascending=False)

# creating the breakout room column & initializing it to zero
df_participants['Breakout Room'] = 0

# reindexing the columns after sorting them
df_participants = df_participants.reindex(columns=['Breakout Room', 'E-Mail', 'Age', 'Preference'])
df_participants = df_participants.reset_index(drop=True)

############################################################################################################
# PREFERENCES INCORPORATED BELOW:
############################################################################################################

# creating lists of preferences and emails for manipulation
pref_indexes = []
email_indexes = []

for pref in df_participants['Preference']:
    if isinstance(pref, str):
        pref_indexes.append(pref.lower())

for email in df_participants['E-Mail']:
    if isinstance(email, str):
        email_indexes.append(email.lower())

# moving preferences next to desired participant & inserting them into the email column
counter1 = 1
counter2 = 0
pref_length = len(pref_indexes) - 1
for pref in pref_indexes:
    if pref in email_indexes:
        temp_email_index = email_indexes.index(pref)
        if temp_email_index > counter2:
            temp_email_value = email_indexes[temp_email_index]

            if pref_length > temp_email_index:
                temp_pref_index = temp_email_index
                temp_pref_value = pref_indexes[temp_pref_index]
                del pref_indexes[temp_pref_index]
                pref_indexes.insert(counter1, temp_pref_value)
            elif pref_length < temp_email_index:
                pref_indexes.insert(counter1, ' ')

            del email_indexes[temp_email_index]

            email_indexes.insert(counter1, temp_email_value)
    counter1 += 1
    counter2 += 1

# replacing the original email list with the new email list that accounts for preferences
email_series = pd.Series(email_indexes)
# print(email_series)
df_participants['E-Mail'] = email_series
# print statement below shows data frame with email, age, and preference

# print(df_participants)

############################################################################################################
# BREAKOUT ROOMS CREATED BELOW:
############################################################################################################

# establishing breakout room size / number of breakout rooms based on requirements (ideal # is 16)
breakout_room_size = 16
num_of_breakout_rooms = int((len(df_participants['E-Mail'])/breakout_room_size))
modulus = len(df_participants['E-Mail']) % breakout_room_size
num_of_participants = len(df_participants['Breakout Room'])

# assigning breakout rooms when # participants divides up evenly
counter = 0
if modulus == 0:
    for num in range(num_of_breakout_rooms):
        for x in range(breakout_room_size):
            df_participants.iloc[counter, 0] = num + 1
            counter += 1

# assigning breakout rooms when # participants DOES NOT divide up evenly
# but CREATING NEW breakout room to account for remaining girls
elif modulus >= 10:
    for num in range(num_of_breakout_rooms):
        for x in range(breakout_room_size):
            df_participants.iloc[counter, 0] = num + 1
            counter += 1

    remainder_breakout_room_num = num_of_breakout_rooms + 1

    final_breakout_room_index = num_of_participants - (num_of_breakout_rooms * 20)

    total_num_participants = final_breakout_room_index + modulus

    total_num_participants_index = total_num_participants - 1

    for x in range(len(df_participants['E-Mail'])):
        if df_participants.iloc[x, 0] == 0:
            df_participants.iloc[x, 0] = remainder_breakout_room_num

# assigning breakout rooms when # participants DOES NOT divide up evenly
# but NOT CREATING NEW breakout room to account for remaining girls
else:

    if modulus <= num_of_breakout_rooms:
        breakout_room_size = breakout_room_size + 1
        for x in range(modulus):
            for i in range(breakout_room_size):
                df_participants.iloc[counter, 0] = x + 1
                counter += 1
        breakout_room_size = breakout_room_size - 1
        for x in range(num_of_breakout_rooms - modulus):
            for i in range(breakout_room_size):
                df_participants.iloc[counter, 0] = x + modulus + 1
                counter += 1

    else:
        breakout_room_size = round(num_of_participants / num_of_breakout_rooms)
        if breakout_room_size * num_of_breakout_rooms < num_of_participants:
            breakout_room_size += 1
        if breakout_room_size <= 18:
            modulus = num_of_participants % num_of_breakout_rooms

            if modulus == 0:
                for num in range(num_of_breakout_rooms):
                    for x in range(breakout_room_size):
                        df_participants.iloc[counter, 0] = num + 1
                        counter += 1
            elif modulus <= num_of_breakout_rooms:

                for x in range(modulus):
                    for i in range(breakout_room_size):
                        df_participants.iloc[counter, 0] = x + 1
                        counter += 1
                breakout_room_size = breakout_room_size - 1
                for x in range(num_of_breakout_rooms - modulus):
                    for i in range(breakout_room_size):
                        df_participants.iloc[counter, 0] = x + modulus + 1
                        counter += 1
        else:
            num_of_breakout_rooms = num_of_breakout_rooms + 1
            breakout_room_size = int(num_of_participants / num_of_breakout_rooms)
            modulus = num_of_participants % num_of_breakout_rooms

            if modulus <= num_of_breakout_rooms:
                breakout_room_size = breakout_room_size + 1
                for x in range(modulus):
                    for i in range(breakout_room_size):
                        df_participants.iloc[counter, 0] = x + 1
                        counter += 1
                breakout_room_size = breakout_room_size - 1
                for x in range(num_of_breakout_rooms - modulus):
                    for i in range(breakout_room_size):
                        df_participants.iloc[counter, 0] = x + modulus + 1
                        counter += 1

# final product printed before exporting to csv
print('\n\n~~~~~Here is what will be in your CSV export:~~~~~\n\n')
print(df_participants)

# asking Kailey to enter file path destination
loop2 = 0
export_file_path = input('\n\nPlease enter the file path of where you want the output CSV to be stored.\n'
                         'File path: ')
while loop2 == 0:
    if isinstance(export_file_path, str) and '/' in export_file_path and '.csv' in export_file_path:
        loop2 = 1
    else:
        print('\n\nPlease enter a valid file path.')
        export_file_path = input('File path: ')
        loop2 = 0

# exporting to csv!!
df_participants.to_csv(export_file_path, index=False)
