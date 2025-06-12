import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置matplotlib默认字体为SimHei，以支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 设置页面标题
st.title("投诉运营数据分析平台")

# 模拟数据
np.random.seed(42)
data = {
    '投诉日期': pd.date_range(start='2024-01-01', periods=180),
    '投诉类型': np.random.choice(['服务态度', '产品质量', '交付延迟', '功能问题', '其他'], size=180),
    '处理状态': np.random.choice(['已解决', '处理中', '未处理'], size=180),
    '处理时长': np.random.randint(1, 100, size=180),
    '满意度评分': np.random.uniform(1, 5, size=180),
    '告警等级': np.random.choice(['低', '中', '高'], size=180)
}
df = pd.DataFrame(data)

# 侧边栏筛选条件
st.sidebar.header("数据筛选")
start_date = st.sidebar.date_input("开始日期", df['投诉日期'].min())
end_date = st.sidebar.date_input("结束日期", df['投诉日期'].max())
# 将date类型转换为datetime类型
start_date = pd.Timestamp.combine(start_date, pd.Timestamp.min.time())
end_date = pd.Timestamp.combine(end_date, pd.Timestamp.max.time())
selected_type = st.sidebar.multiselect("投诉类型", df['投诉类型'].unique())
selected_status = st.sidebar.multiselect("处理状态", df['处理状态'].unique())

# 应用筛选条件
filtered_df = df[(df['投诉日期'] >= start_date) & (df['投诉日期'] <= end_date)]
if selected_type:
    filtered_df = filtered_df[filtered_df['投诉类型'].isin(selected_type)]
if selected_status:
    filtered_df = filtered_df[filtered_df['处理状态'].isin(selected_status)]

# 数据分析模块
st.header("1. 投诉数据分析")
col1, col2 = st.columns(2)
with col1:
    st.subheader("投诉类型分布")
    type_count = filtered_df['投诉类型'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(type_count, labels=type_count.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

with col2:
    st.subheader("处理状态占比")
    status_count = filtered_df['处理状态'].value_counts()
    fig, ax = plt.subplots()
    ax.bar(status_count.index, status_count.values)
    st.pyplot(fig)

# 告警分析模块
st.header("2. 告警分析")
st.subheader("告警等级分布")
alert_count = filtered_df['告警等级'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=alert_count.index, y=alert_count.values, ax=ax)
st.pyplot(fig)

# 数据洞察模块
st.header("3. 数据洞察")
st.subheader("处理时长与满意度关系")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_df, x='处理时长', y='满意度评分', hue='告警等级', ax=ax)
st.pyplot(fig)

st.subheader("投诉趋势分析")
daily_count = filtered_df.groupby('投诉日期').size()
fig, ax = plt.subplots()
ax.plot(daily_count.index, daily_count.values)
ax.set_xlabel("日期")
ax.set_ylabel("投诉数量")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)