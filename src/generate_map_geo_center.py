# IMPORTS
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(111)

# LOAD DATA
data = pd.read_csv('output/tables/speeches_with_coordinates.csv')
final_df = data[data['place']!='MR'] # MR was being incorrectly mapped to Mauritania

final_df['date_obj'] = pd.to_datetime(final_df['date'], utc=True)
final_df['period'] = (final_df['date_obj'].dt.year // 20) * 20

# GENERATE CENTROIDS PER 20-YEARS PERIODS
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

period_data = []
sorted_periods = sorted(final_df['period'].dropna().unique())

for period in sorted_periods:
    subset = final_df[final_df['period'] == period]
    
    lat, lon = get_spherical_centroid(subset['lat'], subset['lon'])
    
    period_data.append({
        'Decade': int(period),
        'Latitude': lat,
        'Longitude': lon
    })

# GENERATE MAP
df_plot = pd.DataFrame(period_data)

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
                s=120,            
                edgecolor='#E2902B', 
                zorder=2,
                marker="o")

for i in range(len(df_plot) - 1):
    start = df_plot.iloc[i]
    end = df_plot.iloc[i+1]
    ax.annotate("", 
                xy=(end['Longitude'], end['Latitude']), 
                xytext=(start['Longitude'], start['Latitude']),
                arrowprops=dict(arrowstyle="->", 
                                color='gray', 
                                lw=1.5,
                                shrinkA=5,
                                shrinkB=5,
                                alpha=0.8))

for i, row in df_plot.iterrows():
    if (True): 
        ax.text(row['Longitude'], row['Latitude'] - (1.5 * np.random.normal(1,0.5)) , 
                str(int(row['Decade'])) + "s", 
                fontsize=10, 
                ha='center', 
                fontweight='bold',
                color="#222222")
        
plt.suptitle(f"Evolution of the Geographical Center of US Presidential Speeches", fontsize=22, fontweight='bold', x=0.5, y=0.98, bbox=dict(facecolor="#FFFFFF00", alpha=0, edgecolor='white'))

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

plt.title("Aggregated for 20-year periods",x=0.5, y=1.01)
plt.tight_layout()

plt.savefig('output/figs/evolution_geo_center.png', dpi=800)