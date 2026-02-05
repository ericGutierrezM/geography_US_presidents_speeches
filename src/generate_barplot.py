# IMPORTS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# LOAD AND PREPARE DATA
data = pd.read_csv('output/tables/speeches_with_coordinates.csv')

data_places = data.groupby('place').agg({'president':'count'})
places_sorted = data_places.sort_values(by='president', ascending=False).reset_index()
places_sorted = places_sorted[places_sorted['place']!='MR'].head(10)

# BUILD GRAPH
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial']

fig, ax = plt.subplots(figsize=(12, 8))

sns.barplot(
    data=places_sorted,
    x='president', 
    y='place', 
    ax=ax,
    color='#A2AFC0',
    alpha=1,
    edgecolor='white',
    linewidth=0.5
)

sns.despine(left=True, bottom=True)

ax.grid(axis='x', color='gray', linestyle='--', linewidth=0.5, alpha=0.4)
ax.set_axisbelow(True) 

ax.tick_params(axis='both', which='both', length=0)

ax.set_xlabel("Number of Mentions", fontsize=10, color='#555555', labelpad=10)

ax.set_ylabel("", fontsize=0)
ax.tick_params(axis='y', labelsize=11, colors='#333333')

plt.suptitle(
    "Top 10 Most Mentioned Places in US Presidents' Speeches (1852-2025)", 
    fontsize=20, 
    fontweight='bold', 
    y=0.99, 
    x=0.5
)

for i, v in enumerate(places_sorted['president']):
    ax.text(
        v + (v * 0.01),       
        i,                    
        str(v),               
        va='center',         
        fontsize=9, 
        color='#555555'
    )

text_content = "© 2026 Eric Gutiérrez | Projection: WGS84 (EPSG:4326)"

plt.figtext(
    0.98, 0.02,                 
    text_content,
    ha="right",               
    va="bottom",              
    fontsize=8,                
    fontstyle='italic',
    color='#555555',            
    bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=2)
)

plt.tight_layout()
plt.savefig(f'output/figs/top10_places_ALL.png', dpi=800, bbox_inches='tight', pad_inches=0.1)