# IMPORTS
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math
import pandas as pd

# LOAD DATA
final_df = pd.read_csv('output/tables/speeches_with_coordinates.csv')


for president in final_df['president'].unique():
    print(f'Generating {president} map...')
    
    # GROUP BY
    df_counts = final_df[final_df['president']==president].groupby(['lat', 'lon']).size().reset_index(name='count')

    # BUILD MAP
    gdf_weighted = gpd.GeoDataFrame(
        df_counts, 
        geometry=gpd.points_from_xy(df_counts.lon, df_counts.lat),
        crs="EPSG:4326"
    )

    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(url)

    fig, ax = plt.subplots(figsize=(15, 12))

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial']

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.tick_params(axis='both', which='both', length=0)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_facecolor("#15159900") 
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.4, zorder=0)

    world.plot(ax=ax, color="#A2AFC0", edgecolor='white', zorder=1, linewidth=0.1)

    scale_factor = 3

    gdf_weighted.plot(
        ax=ax, 
        color='red', 
        markersize=gdf_weighted['count'] * scale_factor, 
        alpha=0.6,
        zorder=5
    )

    legend_sizes = [50, 150, 450] 
    legend_labels = [s for s in legend_sizes]

    legend_handles = [
        Line2D(
            [0], [0], 
            marker='o', 
            color='w', 
            label=label,
            markerfacecolor='red',
            alpha=0.6, 
            markeredgecolor='red',
            markersize=math.sqrt(s * scale_factor)
        ) 
        for s, label in zip(legend_sizes, legend_labels)
    ]

    ax.legend(
        handles=legend_handles, 
        title="Times Mentioned",
        bbox_to_anchor=(0.05, 0.05), 
        loc='lower left', 
        fontsize=12,            
        title_fontsize=14,      
        frameon=True, 
        facecolor='white', 
        edgecolor='white',      
        framealpha=0.7,           
        borderpad=1.7,            
        labelspacing=3.5,
        handletextpad=1.7
    )
    plt.suptitle(f"Places Mentioned in {president}'s Speeches", fontsize=22, fontweight='bold', x=0.5, y=0.83, bbox=dict(facecolor="#FFFFFF00", alpha=0, edgecolor='white'))

    text_content = "© 2026 Eric Gutiérrez | Projection: WGS84 (EPSG:4326)"

    plt.figtext(
        0.98, 0.18,                 
        text_content,
        ha="right",               
        va="bottom",              
        fontsize=8,                
        fontstyle='italic',
        color='#555555',            
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=2)
    )

    plt.tight_layout()
    plt.savefig(f'output/figs/map_places_{president}.png', dpi=800, bbox_inches='tight', pad_inches=0.1)