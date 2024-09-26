##转化Excel文件为指定格式的json文件
import pandas as pd
import json

# 读取Excel文件
excel_path = r"D:\mywork\DataSet\sqldata\QAdata.xlsx"
df = pd.read_excel(excel_path)

# 输出DataFrame的列名
print(df.columns)

# 确认是否包含名为 'Response' 的列
if 'instruction' not in df.columns:
    raise KeyError("No 'instruction' column found in the Excel file.")

# 确认是否包含名为 'case' 的列
if 'input' not in df.columns:
    raise KeyError("No 'input' column found in the Excel file.")
# 确认是否包含名为 'output' 的列
if 'input' not in df.columns:
    raise KeyError("No 'output' column found in the Excel file.")
# 提取instruction,input,output列的数据
data = {}
for index, row in df.iterrows():
    instruction = row['instruction']  # 提取 CASE 列的数据
    input = row['input']  # 提取 Response 列的数据
    output = row['output']  # 提取 Response 列的数据
    data[index]= {
              "instruction": instruction,  # 将 instruction数据作为原始提示存储
              "input": input,  # 将 input 数据作为原始提示存储
              "output": output  # 将 output 数据作为原始提示存储
             }
##提取字典值，转化为没有数字序号的列表字典
list_obj=[]
for key in data.keys():
    list_obj.append(data[key])
print(list_obj)
# 将数据保存为JSON文件，并按照中文形式保存
json_path = r"D:\mywork\DataSet\sqldata\QAdata.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(list_obj, f, ensure_ascii=False, indent=4)

print(f"JSON 文件已生成：{json_path}")
