import streamlit as st
from PIL import Image
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import base64
import os
# 设置页面配置
st.set_page_config(layout="wide")

# 创建侧边栏，并添加身份选择
with st.sidebar:
    st.header('Please select identity')
    identity = st.radio("", ('出展社', '主催者'))

# 根据选择的身份设置内容选项
content_options = {
    '出展社': ['基本情報', '来場者クラスタリング', '自社製品ランキング'],
    '主催者': ['基本情報', '会場内の人流ヒートマップ', '製品、出展社ランキング']
}

# 创建侧边栏的内容选择下拉菜单
with st.sidebar:
    st.header('Please select a view')
    content_selection = st.selectbox("", content_options[identity])

# 创建主页面的内容
st.title('Interop_Tokyo_202306のデータ分析')
st.header(f'Identity：{identity}',divider='rainbow')
st.subheader(f'{content_selection}')

# 在页面上展示其他内容...
# 这里添加你的应用逻辑
def get_base64_encoded_gif(gif_path):
    with open(gif_path, "rb") as gif_file:
        encoded_gif = base64.b64encode(gif_file.read()).decode('utf-8')
    return encoded_gif

# 当你确定路径是相对于allin.py的路径时，可以直接使用
def get_file_path(relative_path):
    return os.path.join("date", relative_path)

# 根据身份和选择显示不同的内容
if identity == '主催者' and content_selection == '会場内の人流ヒートマップ':
    #st.subheader('会場の人流ヒートマップ')

    #data_file_path = 'data/'  # 将文件放在与你的 Streamlit 脚本相同的GitHub仓库中的 'data' 文件夹下
    date_option = st.radio("Date:", ('2023.06.14', '2023.06.15', '2023.06.16'))

    # 添加下拉列表框让用户选择模式
    mode = st.selectbox("modes選択:", ('', 'オートマチック', 'マニュアル'))

    # 检查是否已经选择了模式
    if mode == 'オートマチック':
        # 构建GIF文件名和路径
        gif_date = date_option.replace('.', '')
        gif_filename = f'venue_heatmap_{gif_date}.gif'
        gif_path = get_file_path(gif_filename)

        # 获得Base64编码的GIF
        def get_base64_encoded_gif(gif_path):
            with open(gif_path, "rb") as gif_file:
                encoded_gif = base64.b64encode(gif_file.read()).decode('utf-8')
            return encoded_gif

        encoded_gif = get_base64_encoded_gif(gif_path)

        # 使用HTML <img> 标签和Base64编码显示GIF动图
        gif_html = f'<img src="data:image/gif;base64,{encoded_gif}" alt="Heatmap Animation" style="width: 80%; height: auto;">'
        st.markdown(gif_html, unsafe_allow_html=True)

    elif mode == 'マニュアル':
        # 创建滑动条以选择小时
        hour_selected = st.slider("Hour:", 9, 18, step=1, format="%d:00")

        # 构造对应的热力图文件路径
        date_formatted = date_option.replace('.', '-')
        heatmap_filename = f'venue_heatmap_{date_formatted}_{hour_selected}h.png'
        heatmap_file_path = get_file_path(heatmap_filename)
        # 尝试加载并显示热力图
        try:
            image = Image.open(heatmap_file_path)
            st.image(image, width=700)  # 设置图片大小
        except FileNotFoundError:
            st.error(f"未找到{date_option} {hour_selected}:00的热力图文件。请确保文件存在于指定路径：{heatmap_file_path}")
elif content_selection == '製品、出展社ランキング':
        # 製品、出展社ランキング的代码块...
        data_file_path = 'allend.xlsx'
        data = pd.read_excel(data_file_path)
        data['出展社ID'] = data['出展社ID'].astype(str)

        # 出展社ランキング
        grouped_scores_exhibitor = data.groupby(['出展社名', '出展社ID'])['スコア'].sum().reset_index()
        top10_scores_exhibitor = grouped_scores_exhibitor.nlargest(10, 'スコア')
        fig_exhibitor = px.bar(top10_scores_exhibitor, x='スコア', y='出展社名', text='スコア', orientation='h', color='出展社ID',
                                title="出展社人気ランキング10", color_discrete_sequence=px.colors.qualitative.Set3)
        fig_exhibitor.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_exhibitor.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig_exhibitor, use_container_width=True)

        # 製品ランキング
        grouped_scores_product = data.groupby('製品')['スコア'].sum().reset_index()
        top10_scores_product = grouped_scores_product.nlargest(10, 'スコア')
        top10_ids = data[data['製品'].isin(top10_scores_product['製品'])].drop_duplicates('製品')[['製品', '出展社名']]
        top10_scores_product = top10_scores_product.merge(top10_ids, on='製品')
        fig_product = px.bar(top10_scores_product, x='スコア', y='製品', text='スコア', orientation='h', color='出展社名',
                                title="製品人気ランキング10", color_discrete_sequence=px.colors.qualitative.Prism)
        fig_product.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_product.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig_product, use_container_width=True)
# 根据不同的内容选择显示不同的内容
elif identity == '主催者' and content_selection == '基本情報':


    # 使用columns来创建两栏布局，左侧放置文本信息，右侧放置图片
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<p class="big-font"> <b>🏢 展会名</b></p>', unsafe_allow_html=True)
        st.write('Interop Tokyo 2023')
        st.write('')
        st.markdown('<p class="big-font"> <b>📍 展会地址</b></p>', unsafe_allow_html=True)
        st.write('〒261-8550 千葉県千葉市美浜区中瀬２丁目１')
        st.write('')
        st.markdown('<p class="big-font"> <b>🚉 最近の駅</b></p>', unsafe_allow_html=True)
        st.write('海浜幕張')

        st.write('')
        st.markdown('<p class="big-font"> <b>📅 展示会の日程</b></p>', unsafe_allow_html=True)
        st.write('2023年6月14日(水)～16日(金)')

        st.write('')
        st.markdown('<p class="big-font"> <b>ℹ️ 展会詳細</b></p>', unsafe_allow_html=True)
        st.markdown('[展会詳細はこちら](https://archive.interop.jp/2023/about/)')
        st.write('')
    # 从Excel文件加载公司名单
    companies = pd.read_excel('shikai.xlsx')
    companies_df = pd.DataFrame(companies, columns=['出展社名'])

    # 默认显示的公司数量
    display_count = 3

    st.markdown('<p class="big-font"> <b>📘出展会社の紹介</b></p>', unsafe_allow_html=True)

    # 如果公司数量超过了默认显示数量，使用expander显示剩余部分
    if len(companies_df) > display_count:
        # 显示前display_count个公司
        st.table(companies_df.head(display_count))
    
        # 使用expander来显示更多公司
        with st.expander("さらに表示"):
            st.table(companies_df[display_count:])
    else:
        # 如果公司数量不足默认显示数量，直接显示全部
        st.table(companies_df)
    st.write('')
    st.markdown('<p class="big-font"><b>📘製品の紹介</b></p>', unsafe_allow_html=True)
    st.write("NTT Com DD株式会社は、ネットワークセキュリティとクラウドサービスを提供する先駆者です。")

    # 使用expander来隐藏或显示更多详细信息
    with st.expander("📦 出展製品の詳細"):
        st.write("""
        - **Tufin:** セキュリティポリシー管理を簡素化します。
        - **Managed Security Service for Cisco Secure / Cisco XDR / Cisco SASE:** 統合セキュリティソリューションを提供します。
        """)

    with st.expander("📢 プレゼンテーションのスケジュール"):
        st.write("""
        - 6月14日 13:00 - Cisco Secureのデモ
        - 6月15日 15:00 - セキュリティ戦略に関するパネルディスカッション
        """)
elif identity == '出展社' and content_selection == '基本情報':
 
    st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">🌐 <b>Interop Tokyo 2023 展示会の紹介</b></p>', unsafe_allow_html=True)

    # 使用columns布局来创建更加动态的页面布局
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        **🏢 展会名:** Interop Tokyo 2023  
        **🔗 展会詳細:** [こちら](https://archive.interop.jp/2023/about/)  
        **📅 出展の日付:** 2023年6月14日(水)～16日(金)  
        **🏭 出展の会社数:** 205社  
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        📞 **連絡先**  
        - 電話番号: 03-1234-5678  
        - メール: contact@nttcomdd.jp  
        - [Twitter](https://twitter.com/nttcomdd)  
        """, unsafe_allow_html=True)
    st.write('')  
    st.write('')
    st.markdown('<p class="big-font">🏢 <b>自社の紹介</b></p>', unsafe_allow_html=True)
    st.markdown("""
    - **出展会名:** NTT Com DD株式会社  
    - **出展会社ID:** 555  
    - **出展製品:** Tufin, Managed Security Service for Cisco Secure / Cisco XDR / Cisco SASE  
    - **自社来場者人数:** 1500人、割引5%
    - **ダウンロード回数:** 120回
    - **メール転送回数:** 80回
    """, unsafe_allow_html=True)

    st.write('')
    st.markdown('<p class="big-font">📈 <b>データ紹介</b></p>', unsafe_allow_html=True)
    st.markdown("""
    - **自社来場者人数:** 1500人、割引5%
    - **ダウンロード回数:** 120回
    - **メール転送回数:** 80回
    """, unsafe_allow_html=True)
elif identity == '出展社' and content_selection == '来場者クラスタリング':
    position_toggle = st.toggle("職務", value=False)

    def load_data(toggle):
        if toggle:
            # 如果toggle为开启状态（True），加载考虑职务的数据集
            file_name = 'allend1.xlsx'
        else:
            # 如果toggle为关闭状态（False），加载不考虑职务的数据集
            file_name = 'allend.xlsx'

        df = pd.read_excel(file_name)
        df = df[df['出展社名'] == 'NTT Com DD株式会社']
        return df

    df_final = load_data(position_toggle)

    # 根据用户选择调整的数据加载逻辑后的代码继续
    # 使用toggle状态来决定x_axis的值
    x_axis = '職務スコア' if position_toggle else 'スコア'


    # 使用Plotly创建3D散点图
    fig = px.scatter_3d(df_final, x=x_axis, y='関心度', z='重要度',
                        color='重要度', color_continuous_scale=px.colors.sequential.Viridis)

    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

    # 显示来场者的重要度统计信息
    st.subheader("来場者の重要度を選択してください")
    important_counts = df_final['重要度'].value_counts()
    total_counts = len(df_final)
    important_percentages = (important_counts / total_counts) * 100

    relevance_option = st.radio(
        "",
        ['高', '中高', '中', '低'],
        format_func=lambda x: f"{x} ({important_counts.get(x, 0)}/{total_counts} 約 {important_percentages.get(x, 0):.2f}%)" if x in important_counts else x
    )

    data_display = df_final[df_final['重要度'] == relevance_option]
    # 根据用户的选择调整显示和下载的列
    columns_to_display = ['製品', 'AiTag ID', '関心度', '興味度', 'メモ', '重要度'] if not position_toggle else ['製品', 'AiTag ID', '関心度', 'メモ', '興味度', '職務', '重要度']

    st.write(data_display[columns_to_display])


    # 文件下载部分
    towrite = io.BytesIO()
    downloaded_file = data_display[columns_to_display]
    downloaded_file.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)

    st.download_button(
        label=':inbox_tray: ダウンロード',
        data=towrite,
        file_name="data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
elif identity == '出展社' and content_selection == '自社製品ランキング':
       # 设置Streamlit页面配置
       #st.set_page_config(layout="wide")
       #st.title("データ分析 - 自社製品スコアランキング")

       def load_data():
              # 读取数据，确保路径正确
              df = pd.read_excel('allend.xlsx')
              df = df[['出展社名', '製品', 'スコア']]
              return df

       def prepare_data(df, 自己会社名):
              # 先计算所有製品的总得分
              all_products_scores = df.groupby(['製品', '出展社名'])['スコア'].sum().reset_index()

              # 计算排名
              all_products_scores['Rank'] = all_products_scores['スコア'].rank(method='max', ascending=False)

              # 筛选出自己公司的产品并按排名排序
              自己会社製品 = all_products_scores[all_products_scores['出展社名'] == 自己会社名].sort_values(by='Rank', ascending=True)
              
              return 自己会社製品

       def plot_product_ranking(grouped_scores):
              # 创建图表
              fig = go.Figure()
              
              # 为每个产品绘制条形图
              for _, row in grouped_scores.iterrows():
                     fig.add_trace(go.Bar(
                     x=[row['スコア']],
                     y=[f"{row['製品']} (Top {int(row['Rank'])})"],
                     orientation='h',
                     marker=dict(
                            color='blue',  # 可以根据需要调整颜色
                     )
                     ))
              
              # 更新布局，并隐藏凡例
              fig.update_layout(
                     xaxis={'title': 'スコア'},
                     yaxis={'title': '製品', 'autorange': "reversed"},  # Y轴自动逆序显示
                     title="自社製品スコアランキング",
                     showlegend=False
              )
              return fig

       # 主逻辑
       df = load_data()
       自己会社名 = "NTT Com DD株式会社"  # 根据实际情况修改
       grouped_scores_sorted = prepare_data(df, 自己会社名)
       fig = plot_product_ranking(grouped_scores_sorted)
       st.plotly_chart(fig, use_container_width=True)