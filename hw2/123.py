import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# 讀取地理數據
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# 讀取並合併人口數據
df = pd.read_csv('Global_Population_Gender_Aging_2023.csv')
world = world.merge(df, how="left", left_on="name", right_on="Country")

# 圓餅圖 - 前10人口國
sorted_df = df.sort_values(by='Population 2023', ascending=False)
top_countries = sorted_df.head(10)
plt.figure(figsize=(10, 7))
plt.pie(top_countries['Population 2023'], labels=top_countries['Country'], autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Countries by Population in 2023')
plt.axis('equal')  # 確保圓餅圖是圓形

# 性別比地圖
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(column='Gender Ratio', ax=ax, legend=True,
           legend_kwds={'label': "Gender Ratio (males per 100 females)"},
           cmap='OrRd', missing_kwds={'color': 'lightgrey'})
world.boundary.plot(ax=ax)

# 高齡化人口比例地圖
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.plot(column='Aging Population %', ax=ax, legend=True,
           legend_kwds={'label': "Aging Population % (Percentage of population over 65)"},
           cmap='BuPu', missing_kwds={'color': 'lightgrey'})
world.boundary.plot(ax=ax)

# 顯示圖表
plt.show()
