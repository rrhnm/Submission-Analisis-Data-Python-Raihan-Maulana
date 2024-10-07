import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

main_data_df = pd.read_csv('dashboard/main_data.csv')

st.title('Data Analysis Brazillian E-Commerce Olist Dicoding')
tab1, tab2, tab3 = st.tabs(["Question 1", "Question 2", "Question 3"])

with tab1:
    st.subheader("Bagaimana distribusi/persebaran seller di berbagai state? State mana yang memiliki seller paling banyak dan paling sedikit? Apakah wilayah yang memiliki seller sedikit memiliki biaya logistik yang lebih tinggi?")
    # PLOT 1 Q1: Sellers Distribution per State
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(x='seller_state', y='num_sellers', data=main_data_df, hue='seller_state', palette='viridis', legend=False)

    for p in bar_plot.patches:
        bar_plot.annotate(format(int(p.get_height())), 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='bottom', 
                       fontsize=10, color='black', 
                       xytext=(0, 5), 
                       textcoords='offset points')

    max_value = main_data_df['num_sellers'].max()
    min_value = main_data_df['num_sellers'].min()

    for p in bar_plot.patches:
        if p.get_height() == max_value:
            p.set_facecolor('red')
        elif p.get_height() == min_value:
            p.set_facecolor('blue')

    plt.title('Sellers Distribution per State', fontsize=16)
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Total Sellers', fontsize=12)
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())

    # PLOT 2 Q1: Average Freight Value per State
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(x='seller_state', y='freight_value', data=main_data_df, hue='seller_state', palette='Blues', legend=False)

    max_value = main_data_df['freight_value'].max()
    min_value = main_data_df['freight_value'].min()

    for p in bar_plot.patches:
        if p.get_height() == max_value:
            p.set_facecolor('red')
        elif p.get_height() == min_value:
            p.set_facecolor('blue')
        else:
            p.set_facecolor('lightblue')

    for p in bar_plot.patches:
        bar_plot.annotate(format(round(p.get_height(), 2)), 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha='center', va='bottom', 
                       fontsize=10, color='black', 
                       xytext=(0, 5), 
                       textcoords='offset points')

    plt.title('Average Freight Value per State', fontsize=16)
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Average Freight Value', fontsize=12)
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf()) 

    # PLOT 3 Q1: Correlation between Number of Sellers and Average Freight Value
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=main_data_df, x='num_sellers', y='freight_value', color='blue')

    for line in range(0, main_data_df.shape[0]):
        plt.text(main_data_df.num_sellers[line], 
             main_data_df.freight_value[line], 
             main_data_df.seller_state[line], 
             horizontalalignment='right', size='medium', color='black', weight='semibold')

    plt.title('Correlation between Number of Sellers and Average Freight Value', fontsize=18)
    plt.xlabel('Number of Sellers', fontsize=14)
    plt.ylabel('Average Freight Value', fontsize=14)
    plt.grid(True)
    st.pyplot(plt.gcf())  

with tab2:
    st.subheader("Bagaimana score review dari customer? Berapa score tertinggi, terendah, serta rata-rata dari review Customer? Kategori produk apa yang memiliki score rendah dan score tinggi?")
    
    # PLOT 1 Q2
    filtered_df_review = main_data_df.iloc[0:6][['review_score_1', 'count']]
    filtered_df_review = filtered_df_review[filtered_df_review['review_score_1'].notna() & filtered_df_review['count'].notna()]

    if filtered_df_review.empty:
        st.write("No data.")
    else:
        plt.clf()
        colors = ['red' if x == filtered_df_review['count'].min() else 'blue' if x == filtered_df_review['count'].max() else 'skyblue' for x in filtered_df_review['count']]
        bars = plt.bar(filtered_df_review['review_score_1'], filtered_df_review['count'], color=colors)

    for bar in bars:
        plt.annotate(format(int(bar.get_height())), 
                         (bar.get_x() + bar.get_width() / 2., bar.get_height()), 
                         ha='center', va='bottom', 
                         fontsize=10, color='black', 
                         xytext=(0, 5), 
                         textcoords='offset points')

    plt.title('Distribution of Review Scores', fontsize=16)
    plt.xlabel('Review Score')
    plt.ylabel('Count')
    plt.xticks(filtered_df_review['review_score_1'])
    st.pyplot(plt)

    # PLOT 2 Q2
    filtered_category_df = main_data_df[['product_category_name', 'review_score']]

    unique_categories = filtered_category_df['product_category_name'].dropna().unique()
    selected_categories = st.multiselect('Pilih Kategori Produk:', unique_categories)

    if selected_categories:
        filtered_category_df = filtered_category_df[filtered_category_df['product_category_name'].isin(selected_categories)]

    avg_review_per_category = filtered_category_df.groupby('product_category_name')['review_score'].mean().reset_index()
    categories_to_plot = avg_review_per_category.loc[[avg_review_per_category['review_score'].idxmin(), 
                                                   avg_review_per_category['review_score'].idxmax()]]

    plt.figure(figsize=(10, 7))
    sns.barplot(x='product_category_name', y='review_score', data=categories_to_plot, color='gray')

    for index, row in categories_to_plot.iterrows():
        if row['review_score'] == categories_to_plot['review_score'].min():
            plt.bar(row['product_category_name'], row['review_score'], color='blue')
        elif row['review_score'] == categories_to_plot['review_score'].max():
            plt.bar(row['product_category_name'], row['review_score'], color='red')

    for index, p in enumerate(plt.gca().patches):
        plt.annotate(format(round(p.get_height(), 2)), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', 
                fontsize=10, color='black', 
                xytext=(0, 5), 
                textcoords='offset points')

    plt.title('Highest and Lowest Rated Product Categories', fontsize=16)
    plt.xlabel('Product Category', fontsize=12)
    plt.ylabel('Average Review Score', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


with tab3:
    st.subheader("Bagaimana preferensi metode pembayaran dari pelanggan, dan apakah metode tertentu mempengaruhi nilai transaksi atau frekuensi pembelian?")
    # PLOT 1 Q3
    filtered_payment_avg_df = main_data_df[['payment_type', 'payment_value']]
    filtered_payment_avg_df = filtered_payment_avg_df[filtered_payment_avg_df['payment_value'].notna()]
    filtered_payment_avg_df = filtered_payment_avg_df[filtered_payment_avg_df['payment_type'].notna()]
    filtered_payment_avg_df = filtered_payment_avg_df[filtered_payment_avg_df['payment_type'] != 'not_defined']

    avg_transaction_values = filtered_payment_avg_df.groupby('payment_type')['payment_value'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    colors = ['blue' if value == avg_transaction_values['payment_value'].min() else 
          'red' if value == avg_transaction_values['payment_value'].max() else 'black' 
          for value in avg_transaction_values['payment_value']]

    bar_plot = sns.barplot(x='payment_type', y='payment_value', data=avg_transaction_values, palette=colors, legend=False)

    for index, p in enumerate(bar_plot.patches):
        bar_plot.annotate(format(round(p.get_height(), 2)), 
                     (p.get_x() + p.get_width() / 2., p.get_height()), 
                     ha='center', va='bottom', 
                     fontsize=10, color='black', 
                     xytext=(0, 5), 
                     textcoords='offset points')

    plt.title('Average Transaction Values by Payment Method', fontsize=16)
    plt.xlabel('Payment Method', fontsize=12)
    plt.ylabel('Average Transaction Value', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

    # PLOT 2 Q3
    filtered_purchase_frequency_df = main_data_df[['payment_type_1', 'frequency']]
    filtered_purchase_frequency_df = filtered_purchase_frequency_df[filtered_purchase_frequency_df['frequency'].notna()]
    filtered_purchase_frequency_df = filtered_purchase_frequency_df[filtered_purchase_frequency_df['payment_type_1'].notna()]
    filtered_purchase_frequency_df = filtered_purchase_frequency_df[filtered_purchase_frequency_df['payment_type_1'] != 'not_defined']

    avg_purchase_frequency = filtered_purchase_frequency_df.groupby('payment_type_1')['frequency'].sum().reset_index()

    plt.figure(figsize=(10, 6))
    colors = ['blue' if value == avg_purchase_frequency['frequency'].min() else 
          'red' if value == avg_purchase_frequency['frequency'].max() else 'black' 
          for value in avg_purchase_frequency['frequency']]

    bar_plot = sns.barplot(x='payment_type_1', y='frequency', data=avg_purchase_frequency, palette=colors, legend=False)

    for index, p in enumerate(bar_plot.patches):
        bar_plot.annotate(format(int(p.get_height())), 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', 
                         fontsize=10, color='black', 
                         xytext=(0, 5), 
                         textcoords='offset points')

    plt.title('Purchase Frequency by Payment Method', fontsize=16)
    plt.xlabel('Payment Method', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)