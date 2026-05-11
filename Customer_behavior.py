import pandas as pd
df = pd.read_csv("C:/Data_Analayst_project/customer_shopping_behavior.csv")
print(df.head())
# print(df.describe(include="all"))
print(df.isnull().sum())

# Logic: Fill missing ratings with the Median of each category
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(
    lambda x: x.fillna(x.median())
)

# Logic check: This should now show 0 for Review Rating
print(df.isnull().sum())

#  Convert all column names to snake_case automatically
df.columns  = [col.lower().replace (' ','_') for col in df.columns]
df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'}, inplace = True)

#  See the new clean column names

# Define the labels for our four groups
age_labels = ['Young Adult','Adult','Middle Aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = age_labels)  
print(df['age_group'].value_counts())

frequency_mapping = {
    'Fortnightly':14,
    'Weekly':7,
    'Monthly':30,
    'Quarterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every 3 Months':90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['frequency_of_purchases', 'purchase_frequency_days']].head())
#  To check if the columns are same

are_same = (df['discount_applied'] == df['promo_code_used']).all()
# print(are_same)
if are_same:
    df.drop('promo_code_used', axis=1, inplace=True)
    print("Redundant column 'promo_code_used' has been removed.")

print(df.columns)
from sqlalchemy import create_engine

# 1. THE SHORTCUT: Set your details here once
USER = "postgres"
PASS = "kausar2116"  
HOST = "localhost"
PORT = "5432"
DB_NAME = "Customer_behaviour"

# 2. THE LOGIC: The "Connection String" (Handshake)
# We use an f-string to build that long annoying URL automatically
conn_string = f'postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}'

# 3. THE ENGINE: This is your bridge
engine = create_engine(conn_string)

# 4. THE ACTION: Push your clean df to SQL
# if_exists='replace' means it creates the table or overwrites it
df.to_sql('customer_data', engine, if_exists='replace', index=False)

print("Success! Data pushed to SQL database.")

