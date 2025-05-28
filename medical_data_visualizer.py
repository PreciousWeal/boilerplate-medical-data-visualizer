import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
df['height_m'] = df['height'] / 100
df['BMI'] = df['weight'] / (df['height_m'] ** 2)
df['overweight'] = (df['BMI'] > 25).astype(int)

# 3
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4
def draw_cat_plot():
    
    # 5 Melt the data to long format
    df_cat = pd.melt(
        df,
        id_vars=['cardio'], 
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'],
        var_name='variable', 
        value_name='value'
    )


    # 6. Group by 'cardio', 'variable', and 'value' to count occurrences
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    

    # 7 - Plot using Seaborn
    plot = sns.catplot(
        data=df_cat, 
        x='variable', 
        y='total', 
        hue='value', 
        col='cardio', 
        kind='bar'
    )



    # 8 - Get the figure from the plot
    fig = plot.fig


    # 9 - Save and return
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    # 1. Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &    # diastolic (ap_lo) should not be higher than systolic (ap_hi)
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Drop extra columns if present (e.g. 'BMI', 'height_m')
    df_heat = df_heat.drop(columns=['BMI', 'height_m'], errors='ignore')
    
    # 12
    # 2. Calculate the correlation matrix
    corr = df_heat.corr()

    # 13
    # 3. Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14
    # 4. Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15
    # 5. Draw the heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt='.1f',
        square=True,
        center=0,
        linewidths=0.5,
        cbar_kws={'shrink': 0.5}
    )


    # 16
    fig.savefig('heatmap.png')
    return fig
