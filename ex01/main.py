import pandas as pd

data = pd.read_csv("ex1.csv", header = None)
df = pd.DataFrame(data)

course1_name = data.iloc[0, 0]
course2_name = data.iloc[0, 1]

students_course1 = set(data.iloc[1:, 0].dropna())  # 第一門課的學生名單，移除 NaN 值
students_course2 = set(data.iloc[1:, 1].dropna())  # 第二門課的學生名單，移除 NaN 值

union = students_course1.union(students_course2)  # 聯集
intersection = students_course1.intersection(students_course2)  # 交集
difference1 = students_course1.difference(students_course2)  # 差集（第一門課的學生不在第二門課的學生名單中）
difference2 = students_course2.difference(students_course1)  # 差集（第一門課的學生不在第二門課的學生名單中）

# 打印結果
print(f"課程 '{course1_name}' 的學生名單:\n", students_course1)
print("\n")
print(f"課程 '{course2_name}' 的學生名單:\n", students_course2)
print("\n")
print("兩門課學生的聯集:\n", union)
print("\n")
print("同時上兩門課的學生(交集):\n", intersection)
print("\n")
print("只在課程 '{}' 的學生(差集):\n".format(course1_name), difference1)
print("\n")
print("只在課程 '{}' 的學生(差集):\n".format(course2_name), difference2)
