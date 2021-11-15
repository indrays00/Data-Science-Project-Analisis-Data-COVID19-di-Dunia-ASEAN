#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)

covid_url = "https://dqlab.id/data/covid19_worldwide_2020.json"
df_covid_worldwide = pd.read_json(covid_url)

print("Informasi data frame awal:")
df_covid_worldwide.info()


# In[2]:


df_covid_worldwide = df_covid_worldwide.set_index("date").sort_index()

print("\nInformasi data frame setelah set index kolom date:")
df_covid_worldwide.info()


# In[3]:


df_covid_worldwide.isna().sum()


# In[7]:


df_covid_worldwide.dropna(subset=['geo_id'], inplace=True)

print("\nJumlah missing value tiap kolom setelah didrop:")
print(df_covid_worldwide.isnull().sum())


# In[8]:


# membaca nama negara berdasarkan geo_id
countries_url = "https://dqlab.id/data/country_details.json"
df_countries = pd.read_json(countries_url)
print(df_countries.head())


# In[11]:


df_covid_denormalized = pd.merge(df_covid_worldwide.reset_index(), df_countries, on = "geo_id").set_index("date")
df_covid_denormalized = pd.merge(df_covid_worldwide.reset_index(), df_countries, on = 'geo_id').set_index("date")
print(df_covid_denormalized.head())


# In[12]:


# fatality ratio
df_covid_denormalized["fatality_ratio"] = df_covid_denormalized["deaths"]/df_covid_denormalized["confirmed_cases"]
print(df_covid_denormalized.head())


# In[13]:


# 20 top hight fatality ratio
df_top_20_fatality_rate = df_covid_denormalized.sort_values("fatality_ratio", ascending=False).head(20)
print(df_top_20_fatality_rate[["geo_id","country_name","fatality_ratio"]])


# In[16]:


# 20 top hight fatality ratio on august
df_covid_denormalized_august = df_covid_denormalized.loc["2020-08"].groupby("country_name").sum()

df_covid_denormalized_august["fatality_ratio"] = df_covid_denormalized_august["deaths"]/df_covid_denormalized_august["confirmed_cases"]

df_top_20_fatality_rate_on_august = df_covid_denormalized_august.sort_values("fatality_ratio", ascending=False).head(20)
print(df_top_20_fatality_rate_on_august["fatality_ratio"])


# In[21]:


# Visulisasi negara dengan fatality_ratio tertinggi
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
df_top_20_fatality_rate_on_august["fatality_ratio"].sort_values().plot(kind="barh", color="coral")
plt.title("Top 20 Highest Fatality Rate Countries", fontsize=18, color="b")
plt.xlabel("Fatality Rate", fontsize=14)
plt.ylabel("Country Name", fontsize=14)
plt.grid(axis="x")
plt.tight_layout()
plt.show()


# In[30]:


# select asean country
asean_country_id = ["ID", "MY", "SG", "TH", "VN"]
filter_list = [(df_covid_denormalized["geo_id"]==country_id).to_numpy() for country_id in asean_country_id]
# print(filter_list)
filter_array = np.column_stack(filter_list).sum(axis=1, dtype="bool")
# print(filter_array)
df_covid_denormalized_asean = df_covid_denormalized[filter_array].sort_index()

print("Cek nilai unik di kolom 'country_name':", df_covid_denormalized_asean["country_name"].unique())
print(df_covid_denormalized_asean.head())


# In[31]:


# first case in asean
print("The first case popped up in each of 5 ASEAN countries:")
for country_id in asean_country_id:
    asean_country = df_covid_denormalized_asean[df_covid_denormalized_asean["geo_id"]==country_id]
    first_case = asean_country[asean_country["confirmed_cases"]>0][["confirmed_cases","geo_id","country_name"]]
    print(first_case.head(1))


# In[32]:


# kasus covid yang dimulai pada bulan maret
df_covid_denormalized_asean_march_onward = df_covid_denormalized_asean[df_covid_denormalized_asean.index>="2020-03-01"]
print(df_covid_denormalized_asean_march_onward.head())


# In[36]:


# Visualisasi Kasus COVID-19 di ASEAN dari bulan maret
import seaborn as sns
plt.figure(figsize=(16,6))
sns.lineplot(data=df_covid_denormalized_asean_march_onward, 
             x=df_covid_denormalized_asean_march_onward.index, 
             y="confirmed_cases", 
             hue="country_name",
             linewidth=2)
plt.xlabel('Record Date', fontsize=14)
plt.ylabel('Total Cases', fontsize=14)
plt.title('Comparison of COVID19 Cases in 5 ASEAN Countries', color="b", fontsize=18)
plt.grid()
plt.tight_layout()
plt.show()


# In[ ]:




