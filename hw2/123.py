import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df = pd.read_csv('Global_Population_Gender_Aging_2023.csv')
world = world.merge(df, how="left", left_on="name", right_on="Country")

# 根據人口數量降序排序
sorted_df = df.sort_values(by='Population 2023', ascending=False)

# 選擇人口數量最多的前10個國家
top_countries = sorted_df.head(10)

# 創建圓餅圖
plt.figure(figsize=(10, 7))
plt.pie(top_countries['Population 2023'], labels=top_countries['Country'], autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Countries by Population in 2023')
plt.axis('equal')  # 確保圓餅圖是圓形

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
world.plot(column='Gender Ratio', ax=ax, legend=True,
           legend_kwds={'label': "Gender Ratio (males per 100 females)"},
           cmap='OrRd', missing_kwds={'color': 'lightgrey'})

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax)
world.plot(column='Aging Population %', ax=ax, legend=True,
           legend_kwds={'label': "Aging Population % (Percentage of population over 65)"},
           cmap='BuPu', missing_kwds={'color': 'lightgrey'})

# 顯示圖表
plt.show()