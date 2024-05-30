import pandas as pd
import jieba
from collections import Counter
import json
import openai
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.cm import get_cmap

# 設置字體
font_path = 'setofont.ttf'  # 替換為你的字體文件路徑
prop = fm.FontProperties(fname=font_path)

# 更新 matplotlib 配置
plt.rcParams.update({
    'font.family': prop.get_name(),
    'axes.unicode_minus': False  # 避免坐標軸負號顯示問題
})

# 读入CSV和JSON文件
df_csv = pd.read_csv('setn_news.csv')
with open('setn_news.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)

# 整合数据
df = pd.concat([df_csv, pd.DataFrame(data_json)], ignore_index=True)

# 断词并计算词频
def get_word_frequency(text):
    words = jieba.lcut(text)
    words = [word for word in words if len(word) > 1]  # 过滤掉单个字符的词
    return Counter(words)

df['WordFrequency'] = df['Content'].apply(get_word_frequency)

# 获取前几个高频词
def get_top_keywords(word_freq, top_n=10):
    return dict(word_freq.most_common(top_n))

df['TopKeywords'] = df['WordFrequency'].apply(lambda x: get_top_keywords(x, top_n=10))

# 使用OpenAI API生成摘要
openai.api_key = ''  # 请替换为你的OpenAI API密钥

def get_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "請提供以下新聞摘要。"},
            {"role": "user", "content": text}
        ],
        max_tokens=200
    )
    summary = response.choices[0].message['content'].strip()
    return summary

df['Summary'] = df['Content'].apply(get_summary)

# 输出处理后的DataFrame
df.to_csv('setn_news_out.csv', index=False)
df.to_json('setn_news_out.json', orient='records')

# 导出DataFrame供其他模块使用
def get_processed_data():
    return df

# 获取处理后的DataFrame
df = get_processed_data()

# 创建关联图
G = nx.Graph()

for index, row in df.iterrows():
    for word in row['TopKeywords']:
        G.add_node(word)
    for word1 in row['TopKeywords']:
        for word2 in row['TopKeywords']:
            if word1 != word2:
                G.add_edge(word1, word2, weight=row['TopKeywords'][word1])

# 计算节点的度数和使用社区发现算法划分社区
degree = dict(G.degree())
communities = nx.algorithms.community.greedy_modularity_communities(G)
community_map = {}
for i, community in enumerate(communities):
    for node in community:
        community_map[node] = i

# 设定颜色映射
cmap = get_cmap('tab20')
colors = [cmap(community_map[node]) for node in G.nodes()]

# 画出关联图
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.5)
nx.draw_networkx_nodes(G, pos, node_size=[degree[node] * 20 for node in G.nodes()], node_color=colors)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

# 手動設置每個標籤的字體
labels = {node: node for node in G.nodes()}
for label, (x, y) in pos.items():
    plt.text(x, y, label, fontsize=12, fontproperties=prop, ha='center', va='center')

plt.title('新聞', fontproperties=prop)
plt.show()

print(df[['Title', 'Summary']])
