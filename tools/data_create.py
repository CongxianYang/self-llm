import pandas
import pandas as pd
from pandas import Series,DataFrame
global sum #设置全局值

df_brand=pd.read_excel("D:\mywork\DataSet\sqldata\dbbrand.xlsx")
print(df_brand.head())
df_qus=pd.read_excel("D:\mywork\DataSet\sqldata\dbQ.xlsx")
print(df_qus.head())
brand=df_brand['brand_name']
#要存入的数据
data={'instruction':['请帮我提取这句话的关键词'],
        'input':['你好'],
        'output':['你好']}
our_df=DataFrame(data)#存为dataframe格式
##遍历替换
print("********************** start replacing *********************")
sum=0

keys=['，综艺，剧集。',
      '，投放效果，曝光量，热搜情况,热搜次数。',
      '，近期，负面消息,正面消息。',
      '，受欢迎，内容，热门文章。',
      '，今年，综艺节目，广告。']

for brname in df_brand.loc[:5000]['brand_name']:
   flag =0
   for qs in df_qus.loc[:]['question']:
       lens=len(qs)
       for i in range(lens):
           if qs[i:i + 7] == '{brand}':
               qs = qs[:i] + brname + qs[i + 7:]
               new_name=brname+keys[flag]
               our_df.loc[sum]=['请帮我提取这句话的关键词',qs,new_name]
               flag=flag+1
               sum=sum+1
               break
print(our_df.head())
print("********************** start storage *********************")
our_df.to_excel("D:\mywork\DataSet\sqldata\QAdata.xlsx",index=False)
print("********************** end storage ********************")

