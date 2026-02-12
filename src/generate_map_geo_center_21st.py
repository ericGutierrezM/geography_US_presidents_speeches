# IMPORTS
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

np.random.seed(111)

# LOAD DATA
data = pd.read_csv('../output/tables/speeches_with_coordinates.csv')
final_df = data[data['place']!='MR'] # MR was being incorrectly mapped to Mauritania

# COMPUTE CENTROIDS
def get_spherical_centroid(lats, lons):
    lat_rad = np.deg2rad(lats)
    lon_rad = np.deg2rad(lons)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    
    x_avg, y_avg, z_avg = np.mean(x), np.mean(y), np.mean(z)
    
    lon_mean = np.arctan2(y_avg, x_avg)
    lat_mean = np.arcsin(z_avg)
    return np.rad2deg(lat_mean), np.rad2deg(lon_mean)

president_data = []
presidents_of_interest = ['Bill Clinton', 'George W. Bush', 'Barack Obama', 'Donald Trump', 'Joe Biden']
for president in final_df['president'].unique():
    if(president in presidents_of_interest):
        subset = final_df[final_df['president'] == president]
        
        lat, lon = get_spherical_centroid(subset['lat'], subset['lon'])
        
        president_data.append({
            'President': president,
            'Latitude': lat,
            'Longitude': lon
        })

# GENERATE MAP
df_plot = pd.DataFrame(president_data)

fig, ax = plt.subplots(figsize=(15, 8))

url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial']

ax.set_xticklabels([])
ax.set_yticklabels([])

ax.tick_params(axis='both', which='both', length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_facecolor("#15159900") 
ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.4, zorder=5)

world.plot(ax=ax, color="#A2AFC0", edgecolor='white', zorder=1, linewidth=0.1)

ax.set_xlim([-135, 10]) 
ax.set_ylim([2, 70])

sc = ax.scatter(df_plot['Longitude'], df_plot['Latitude'],
                color="#E2902B", 
                s=150,            
                edgecolor='#E2902B', 
                zorder=2,
                marker="o")

for i, row in df_plot.iterrows():
    if (True): 
        ax.text(row['Longitude'], row['Latitude'] +1 , 
                row['President'], 
                fontsize=12, 
                ha='center', 
                fontweight='bold',
                color="#222222")
        
plt.suptitle(f"Evolution of the Geographical Center of US Presidential Speeches (21st Century)", fontsize=22, fontweight='bold', x=0.5, y=0.96, bbox=dict(facecolor="#FFFFFF00", alpha=0, edgecolor='white'))

text_content = "© 2026 Eric Gutiérrez | Projection: WGS84 (EPSG:4326)"

plt.figtext(
    0.98, 0.04,                 
    text_content,
    ha="right",               
    va="bottom",              
    fontsize=8,                
    fontstyle='italic',
    color='#555555',            
    bbox=dict(facecolor='white', alpha=0.5, edgecolor='none', pad=2)
)

plt.tight_layout()

plt.savefig('../output/figs/geo_center_presidents_21st.png', dpi=800)