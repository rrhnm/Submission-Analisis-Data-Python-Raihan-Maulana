import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

main_data_df = pd.read_csv('dashboard/main_data.csv')

st.title('E-Commerce Data Analysis Submission')
col1, col2 = st.columns(2)

# SELLERS STATE PLOT
with col1:
    st.header('Seller State Distribution')
    state_counts = main_data_df['seller_state'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=state_counts.index, y=state_counts.values, ax=ax)
    ax.set_xlabel('State')
    ax.set_ylabel('Frequency')
    ax.set_xticklabels(state_counts.index, rotation=45)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='baseline')
    st.pyplot(fig)

# REVIEW SCORE PLOT
with col2:
    st.header('Review Score Distribution')
    max_score = main_data_df['review_score'].max()
    min_score = main_data_df['review_score'].min()
    avg_score = main_data_df['review_score'].mean()

    fig, ax = plt.subplots()
    counts, bins, patches = ax.hist(main_data_df['review_score'], bins=5, edgecolor='black')
    ax.set_xlabel('Review Score')
    ax.set_ylabel('Frequency')
    ax.set_xticks(range(1, 6))
    for count, x in zip(counts, bins):
        ax.text(x + 0.25, count, int(count), ha='center', va='bottom')
    st.pyplot(fig)
    st.write(f'Max Score: {max_score}')
    st.write(f'Min Score: {min_score}')
    st.write(f'AVG Score: {avg_score:.2f}')