import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
csv_file    = os.path.join(os.path.dirname(os.path.abspath(__file__)),'fcc-forum-pageviews.csv')
df          = pd.read_csv(csv_file,
                          index_col = "date", # Set this column as index
                          parse_dates = True  # Convert date from string to actual date
                         )

# Clean data
df  = df[
        (df['value'] <= df['value'].quantile(0.975)) &
        (df['value'] >= df['value'].quantile(0.025))  
        ]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    # Data for plotting
    x = df.index
    y = df['value']

    # Create axis plot
    ax.plot(x, y)
    ax.set(xlabel   = 'Date', 
           ylabel   = 'Page Views',
           title    = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year']  = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    month_order = ['January', 'February', 'March'    , 'April'  , 'May'     , 'June', 
                   'July'   , 'August'  , 'September', 'October', 'November', 'December'
                  ]

    df_bar = df_bar.reindex(columns = month_order)

    # Draw bar plot
    ax = df_bar.plot(kind = 'bar')

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20, 7)) # 2 graphs side by side

    # Year graph
    sns.boxplot(
                data = df_box,
                x ='year',
                y ='value',
                ax = axes[0]
                )

    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month graph
    month_order = ['Jan', 'Feb', 'Mar', 'Apr',
                   'May', 'Jun', 'Jul', 'Aug',
                   'Sep', 'Oct', 'Nov', 'Dec'
                  ]

    sns.boxplot(
                data = df_box,
                x = 'month',
                y = 'value',
                order = month_order,
                ax = axes[1]
            )

    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
