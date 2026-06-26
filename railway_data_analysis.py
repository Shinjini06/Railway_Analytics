import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

CSV_FILE = 'Railway_info.csv'

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class DataExploration:
    
    def __init__(self, filepath):
        print("\n" + "="*70)
        print("LEVEL 1: DATA EXPLORATION AND BASIC OPERATIONS")
        print("="*70)
        
        self.df = pd.read_csv(filepath)
        print(f"\n✓ Dataset loaded successfully!")
        print(f"✓ Dataset shape: {self.df.shape} (rows, columns)")
        
    def task_1_1_inspect_data(self):
        print("\n--- TASK 1.1: Data Inspection ---")
        
        print("\nFirst 10 rows:")
        print(self.df.head(10).to_string())
        
        print("\n\nData Types:")
        print(self.df.dtypes)
        
        print("\n\nDataset Info:")
        print(f"Total Rows: {len(self.df)}")
        print(f"Total Columns: {len(self.df.columns)}")
        print(f"Column Names: {list(self.df.columns)}")
        
        print("\n\nMissing Values:")
        missing = self.df.isnull().sum()
        if missing.sum() == 0:
            print("✓ No missing values found!")
        else:
            print(missing)
            
    def task_1_2_basic_statistics(self):
        print("\n--- TASK 1.2: Basic Statistics ---")
        
        num_trains = self.df['Train_No'].nunique()
        unique_sources = self.df['Source_Station_Name'].nunique()
        unique_destinations = self.df['Destination_Station_Name'].nunique()
        
        print(f"\n✓ Number of unique trains: {num_trains}")
        print(f"✓ Number of unique source stations: {unique_sources}")
        print(f"✓ Number of unique destination stations: {unique_destinations}")
        
        print("\nTop 10 Most Common Source Stations:")
        source_counts = self.df['Source_Station_Name'].value_counts().head(10)
        for idx, (station, count) in enumerate(source_counts.items(), 1):
            print(f"  {idx}. {station}: {count} trains")
        
        print("\nTop 10 Most Common Destination Stations:")
        dest_counts = self.df['Destination_Station_Name'].value_counts().head(10)
        for idx, (station, count) in enumerate(dest_counts.items(), 1):
            print(f"  {idx}. {station}: {count} trains")
        
        print("\nTrains by Operating Day:")
        days_count = self.df['days'].value_counts()
        for day, count in days_count.items():
            print(f"  {day}: {count} trains")
    
    def task_1_3_data_cleaning(self):
        print("\n--- TASK 1.3: Data Cleaning ---")
        
        print("\nChecking for missing values...")
        if self.df.isnull().sum().sum() == 0:
            print("✓ No missing values detected!")
        else:
            print(self.df.isnull().sum())
        
        print("\nStandardizing station names to uppercase...")
        self.df['Source_Station_Name'] = self.df['Source_Station_Name'].str.upper()
        self.df['Destination_Station_Name'] = self.df['Destination_Station_Name'].str.upper()
        self.df['Train_Name'] = self.df['Train_Name'].str.upper()
        self.df['days'] = self.df['days'].str.upper()
        
        print("✓ Station names standardized!")
        
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        print(f"✓ Removed {initial_rows - len(self.df)} duplicate rows")
        
        print("\nCleaned dataset preview:")
        print(self.df.head(5).to_string())
        
        return self.df

class DataTransformation:
    
    def __init__(self, df):
        print("\n" + "="*70)
        print("LEVEL 2: DATA TRANSFORMATION AND AGGREGATION")
        print("="*70)
        self.df = df.copy()
        
    def task_2_1_filtering(self):
        print("\n--- TASK 2.1: Data Filtering ---")
        
        print("\nTrains operating on SATURDAY:")
        saturday_trains = self.df[self.df['days'] == 'SATURDAY']
        print(f"✓ Found {len(saturday_trains)} Saturday trains")
        print(saturday_trains[['Train_No', 'Train_Name', 'Source_Station_Name', 
                               'Destination_Station_Name']].head(10).to_string())
        
        most_common_station = self.df['Source_Station_Name'].value_counts().index[0]
        print(f"\n\nTrains starting from {most_common_station}:")
        station_trains = self.df[self.df['Source_Station_Name'] == most_common_station]
        print(f"✓ Found {len(station_trains)} trains from this station")
        print(station_trains[['Train_No', 'Train_Name', 'Destination_Station_Name', 
                              'days']].head(10).to_string())
        
        return saturday_trains, station_trains
    
    def task_2_2_grouping_aggregation(self):
        print("\n--- TASK 2.2: Grouping and Aggregation ---")
        
        print("\nTrains originating from each source station:")
        source_agg = self.df.groupby('Source_Station_Name').size().reset_index(name='Train_Count')
        source_agg = source_agg.sort_values('Train_Count', ascending=False)
        print(source_agg.head(15).to_string())
        
        print("\n\nTrain count by day of week:")
        day_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        day_agg = self.df.groupby('days').size().reset_index(name='Train_Count')
        day_agg['days'] = pd.Categorical(day_agg['days'], categories=day_order, ordered=True)
        day_agg = day_agg.sort_values('days')
        print(day_agg.to_string())
        
        return source_agg, day_agg
    
    def task_2_3_enrichment(self):
        print("\n--- TASK 2.3: Data Enrichment ---")
        
        weekend_days = {'SATURDAY', 'SUNDAY'}
        self.df['Day_Category'] = self.df['days'].apply(
            lambda x: 'WEEKEND' if x in weekend_days else 'WEEKDAY'
        )
        
        print("\nTrain distribution by day category:")
        category_dist = self.df['Day_Category'].value_counts()
        for cat, count in category_dist.items():
            percentage = (count / len(self.df)) * 100
            print(f"  {cat}: {count} trains ({percentage:.2f}%)")
        
        self.df['Is_Local'] = (self.df['Source_Station_Name'] == 
                               self.df['Destination_Station_Name']).astype(int)
        
        print(f"\nLocal trains (same source and destination): {self.df['Is_Local'].sum()}")
        print(f"Inter-city trains: {(1 - self.df['Is_Local']).sum()}")
        
        print("\nEnriched dataset preview:")
        print(self.df[['Train_No', 'Source_Station_Name', 'Destination_Station_Name', 
                       'days', 'Day_Category', 'Is_Local']].head(10).to_string())
        
        return self.df

class AdvancedAnalysis:
    
    def __init__(self, df):
        print("\n" + "="*70)
        print("LEVEL 3: ADVANCED DATA ANALYSIS")
        print("="*70)
        self.df = df.copy()
        
    def task_3_1_pattern_analysis(self):
        print("\n--- TASK 3.1: Pattern Analysis ---")
        
        print("\nTrain distribution throughout the week:")
        day_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        day_dist = self.df['days'].value_counts().reindex(day_order)
        
        for day, count in day_dist.items():
            bar_length = int(count / 100)
            print(f"  {day:12}: {count:5} trains |" + "█" * bar_length)
        
        print("\n\nTop 15 Source-Destination Pairs:")
        route_pairs = self.df.groupby(['Source_Station_Name', 'Destination_Station_Name']).size()\
                             .reset_index(name='Count').sort_values('Count', ascending=False)
        print(route_pairs.head(15).to_string())
        
        print("\n\nMost popular routes by day of week:")
        for day in day_order[:3]:
            day_routes = self.df[self.df['days'] == day]\
                        .groupby(['Source_Station_Name', 'Destination_Station_Name']).size()\
                        .reset_index(name='Count').sort_values('Count', ascending=False).head(3)
            print(f"\n  {day}:")
            for _, row in day_routes.iterrows():
                print(f"    {row['Source_Station_Name']} → {row['Destination_Station_Name']}: {row['Count']} trains")
    
    def task_3_2_correlation_insights(self):
        print("\n--- TASK 3.2: Correlation and Insights ---")
        
        print("\nKey Insights:")
        
        train_per_day = self.df['days'].value_counts()
        peak_day = train_per_day.idxmax()
        peak_count = train_per_day.max()
        print(f"\n1. Peak Operating Day:")
        print(f"   {peak_day} has the maximum trains: {peak_count}")
        
        weekend_trains = self.df[self.df['Day_Category'] == 'WEEKEND'].shape[0]
        weekday_trains = self.df[self.df['Day_Category'] == 'WEEKDAY'].shape[0]
        print(f"\n2. Weekday vs Weekend Analysis:")
        print(f"   Weekday trains: {weekday_trains} ({weekday_trains/len(self.df)*100:.2f}%)")
        print(f"   Weekend trains: {weekend_trains} ({weekend_trains/len(self.df)*100:.2f}%)")
        
        top_source = self.df['Source_Station_Name'].value_counts().index[0]
        top_source_count = self.df['Source_Station_Name'].value_counts().iloc[0]
        print(f"\n3. Most Connected Source Station:")
        print(f"   {top_source} with {top_source_count} trains")
        
        local_trains = self.df['Is_Local'].sum()
        print(f"\n4. Journey Type Distribution:")
        print(f"   Local trains: {local_trains} ({local_trains/len(self.df)*100:.2f}%)")
        print(f"   Inter-city trains: {len(self.df)-local_trains} ({(len(self.df)-local_trains)/len(self.df)*100:.2f}%)")
        
        return train_per_day

class Visualization:
    
    def __init__(self, df):
        print("\n" + "="*70)
        print("LEVEL 4: DATA VISUALIZATION AND REPORTING")
        print("="*70)
        self.df = df.copy()
        self.figures = []
        
    def task_4_1_visualizations(self):
        print("\n--- TASK 4.1: Creating Visualizations ---")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        day_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        day_counts = self.df['days'].value_counts().reindex(day_order)
        colors = ['#3498db' if day not in ['SATURDAY', 'SUNDAY'] else '#e74c3c' for day in day_order]
        
        bars = ax.bar(day_order, day_counts.values, color=colors, alpha=0.8, edgecolor='black')
        ax.set_title('Distribution of Trains by Day of Week', fontsize=16, fontweight='bold')
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Number of Trains', fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('viz_1_trains_by_day.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: viz_1_trains_by_day.png")
        plt.close()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        top_sources = self.df['Source_Station_Name'].value_counts().head(15)
        ax.barh(range(len(top_sources)), top_sources.values, color='#2ecc71', alpha=0.8, edgecolor='black')
        ax.set_yticks(range(len(top_sources)))
        ax.set_yticklabels(top_sources.index, fontsize=10)
        ax.set_xlabel('Number of Trains', fontsize=12)
        ax.set_title('Top 15 Source Stations', fontsize=16, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
        
        for i, v in enumerate(top_sources.values):
            ax.text(v + 2, i, str(v), va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('viz_2_top_source_stations.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: viz_2_top_source_stations.png")
        plt.close()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        top_dests = self.df['Destination_Station_Name'].value_counts().head(15)
        ax.barh(range(len(top_dests)), top_dests.values, color='#9b59b6', alpha=0.8, edgecolor='black')
        ax.set_yticks(range(len(top_dests)))
        ax.set_yticklabels(top_dests.index, fontsize=10)
        ax.set_xlabel('Number of Trains', fontsize=12)
        ax.set_title('Top 15 Destination Stations', fontsize=16, fontweight='bold')
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3)
        
        for i, v in enumerate(top_dests.values):
            ax.text(v + 2, i, str(v), va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('viz_3_top_destination_stations.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: viz_3_top_destination_stations.png")
        plt.close()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        category_counts = self.df['Day_Category'].value_counts()
        colors_pie = ['#3498db', '#e74c3c']
        ax1.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%',
               colors=colors_pie, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax1.set_title('Weekday vs Weekend Distribution', fontsize=14, fontweight='bold')
        
        ax2.bar(category_counts.index, category_counts.values, color=colors_pie, alpha=0.8, edgecolor='black')
        ax2.set_ylabel('Number of Trains', fontsize=12)
        ax2.set_title('Weekday vs Weekend Count', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(category_counts.values):
            ax2.text(i, v + 50, str(v), ha='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('viz_4_weekday_weekend.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: viz_4_weekday_weekend.png")
        plt.close()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        journey_counts = self.df['Is_Local'].value_counts()
        journey_labels = ['Inter-city Trains', 'Local Trains']
        colors_journey = ['#1abc9c', '#f39c12']
        
        wedges, texts, autotexts = ax.pie(journey_counts.values, labels=journey_labels, autopct='%1.1f%%',
                                           colors=colors_journey, startangle=90, 
                                           textprops={'fontsize': 12, 'fontweight': 'bold'})
        ax.set_title('Distribution of Train Types', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('viz_5_train_types.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: viz_5_train_types.png")
        plt.close()
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        top_sources_list = self.df['Source_Station_Name'].value_counts().head(10).index
        top_dests_list = self.df['Destination_Station_Name'].value_counts().head(10).index
        
        pivot_data = self.df[(self.df['Source_Station_Name'].isin(top_sources_list)) &
                            (self.df['Destination_Station_Name'].isin(top_dests_list))]\
                    .pivot_table(index='Source_Station_Name', 
                                columns='Destination_Station_Name', 
                                aggfunc='size', fill_value=0)
        
        sns.heatmap(pivot_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Number of Trains'})
        ax.set_title('Heatmap of Top Source-Destination Pairs', fontsize=14, fontweight='bold')
        ax.set_xlabel('Destination Station', fontsize=11)
        ax.set_ylabel('Source Station', fontsize=11)
        
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('viz_6_heatmap_routes.png', dpi=300, bbox_inches='tight')
        print("✓ Saved: viz_6_heatmap_routes.png")
        plt.close()
    
    def task_4_2_generate_report(self):
        print("\n--- TASK 4.2: Generating Comprehensive Report ---")
        
        report = """
╔════════════════════════════════════════════════════════════════════════════╗
║              RAILWAY DATA ENGINEERING - COMPREHENSIVE REPORT               ║
╚════════════════════════════════════════════════════════════════════════════╝

EXECUTIVE SUMMARY
─────────────────────────────────────────────────────────────────────────────
This report presents a comprehensive analysis of railway operational data, 
encompassing data exploration, transformation, advanced analytics, and 
visualization. The dataset contains information about train schedules, routes,
and operating patterns across Indian Railways.

DATASET OVERVIEW
─────────────────────────────────────────────────────────────────────────────
"""
        report += f"Total Records: {len(self.df):,}\n"
        report += f"Data Points (Features): {len(self.df.columns)}\n"
        report += f"Unique Trains: {self.df['Train_No'].nunique():,}\n"
        report += f"Unique Source Stations: {self.df['Source_Station_Name'].nunique():,}\n"
        report += f"Unique Destination Stations: {self.df['Destination_Station_Name'].nunique():,}\n"
        report += f"Operating Days Covered: {self.df['days'].nunique()}\n"
        
        report += "\n" + "─"*80 + "\n"
        report += "KEY STATISTICS\n"
        report += "─"*80 + "\n\n"
        
        day_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
        report += "1. Train Distribution by Day of Week:\n"
        for day in day_order:
            count = len(self.df[self.df['days'] == day])
            percentage = (count / len(self.df)) * 100
            report += f"   • {day:12}: {count:5,} trains ({percentage:5.2f}%)\n"
        
        report += "\n2. Weekday vs Weekend Analysis:\n"
        weekend_count = len(self.df[self.df['Day_Category'] == 'WEEKEND'])
        weekday_count = len(self.df[self.df['Day_Category'] == 'WEEKDAY'])
        report += f"   • Weekday Trains: {weekday_count:,} ({weekday_count/len(self.df)*100:.2f}%)\n"
        report += f"   • Weekend Trains: {weekend_count:,} ({weekend_count/len(self.df)*100:.2f}%)\n"
        
        report += "\n3. Journey Type Distribution:\n"
        local_count = self.df['Is_Local'].sum()
        intercity_count = len(self.df) - local_count
        report += f"   • Local Trains: {local_count:,} ({local_count/len(self.df)*100:.2f}%)\n"
        report += f"   • Inter-city Trains: {intercity_count:,} ({intercity_count/len(self.df)*100:.2f}%)\n"
        
        report += "\n" + "─"*80 + "\n"
        report += "TOP STATIONS\n"
        report += "─"*80 + "\n\n"
        
        report += "Top 10 Source Stations:\n"
        for idx, (station, count) in enumerate(self.df['Source_Station_Name'].value_counts().head(10).items(), 1):
            report += f"   {idx:2}. {station:40} ({count:4,} trains)\n"
        
        report += "\nTop 10 Destination Stations:\n"
        for idx, (station, count) in enumerate(self.df['Destination_Station_Name'].value_counts().head(10).items(), 1):
            report += f"   {idx:2}. {station:40} ({count:4,} trains)\n"
        
        report += "\n" + "─"*80 + "\n"
        report += "TOP ROUTES\n"
        report += "─"*80 + "\n\n"
        
        report += "Top 10 Source-Destination Pairs:\n"
        route_pairs = self.df.groupby(['Source_Station_Name', 'Destination_Station_Name']).size()\
                             .reset_index(name='Count').sort_values('Count', ascending=False)
        for idx, row in route_pairs.head(10).iterrows():
            report += f"   • {row['Source_Station_Name']:30} → {row['Destination_Station_Name']:30} ({row['Count']:4,})\n"
        
        report += "\n" + "─"*80 + "\n"
        report += "INSIGHTS & RECOMMENDATIONS\n"
        report += "─"*80 + "\n\n"
        
        peak_day = self.df['days'].value_counts().idxmax()
        peak_count = self.df['days'].value_counts().max()
        
        report += f"""
1. PEAK OPERATIONAL PATTERNS:
   • {peak_day} records the highest number of trains ({peak_count:,} trains)
   • This suggests maximum passenger demand on this day
   • Recommendation: Deploy additional resources and staff on {peak_day}s

2. WEEKDAY vs WEEKEND OPERATIONS:
   • Weekday operations are {weekday_count/weekend_count:.2f}x higher than weekends
   • This reflects regular commuter patterns and business travel
   • Recommendation: Maintain dedicated weekday fleet while weekend trains can be 
     flexible and premium-service focused

3. STATION CONNECTIVITY:
   • Top source stations handle significant traffic volume
   • Limited connectivity from smaller stations suggests growth opportunities
   • Recommendation: Consider expanding routes from underutilized stations

4. LOCAL vs INTER-CITY BALANCE:
   • {intercity_count/local_count:.2f}% ratio of inter-city to local trains
   • Inter-city trains form the backbone of long-distance connectivity
   • Recommendation: Maintain balanced fleet mix for both local and long-distance travel

5. ROUTE OPTIMIZATION:
   • Top 10 routes account for significant portion of traffic
   • Recommendation: Optimize scheduling and resource allocation for high-traffic routes
   • Consider dynamic pricing and capacity management

VISUALIZATIONS GENERATED
─────────────────────────────────────────────────────────────────────────────
✓ viz_1_trains_by_day.png        - Day-wise distribution
✓ viz_2_top_source_stations.png   - Top 15 source stations
✓ viz_3_top_destination_stations.png - Top 15 destination stations
✓ viz_4_weekday_weekend.png       - Weekday vs weekend comparison
✓ viz_5_train_types.png           - Local vs inter-city distribution
✓ viz_6_heatmap_routes.png        - Source-destination heatmap

CONCLUSION
─────────────────────────────────────────────────────────────────────────────
This comprehensive analysis reveals clear patterns in railway operations:
• Strong weekday demand reflecting commuter needs
• Concentrated traffic on specific high-demand routes
• Significant role of inter-city trains in the network
• Opportunities for capacity optimization and service enhancement

The visualizations and metrics provide actionable insights for operational 
planning, resource allocation, and strategic decision-making.

════════════════════════════════════════════════════════════════════════════════
Report Generated: Railway Data Engineering Project Analysis
"""
        
        with open('RAILWAY_ANALYSIS_REPORT.txt', 'w', encoding='utf-8') as f:
             f.write(report)
        
        print("✓ Report saved to: RAILWAY_ANALYSIS_REPORT.txt")
        print("\n" + report)
        
        return report


def main():
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "RAILWAY DATA ENGINEERING PROJECT - COMPLETE ANALYSIS".center(78) + "║")
    print("║" + "Levels 1-4: From Exploration to Reporting".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    explorer = DataExploration(CSV_FILE)
    explorer.task_1_1_inspect_data()
    explorer.task_1_2_basic_statistics()
    df_cleaned = explorer.task_1_3_data_cleaning()
    
    transformer = DataTransformation(df_cleaned)
    saturday_trains, station_trains = transformer.task_2_1_filtering()
    source_agg, day_agg = transformer.task_2_2_grouping_aggregation()
    df_enriched = transformer.task_2_3_enrichment()
    
    analyzer = AdvancedAnalysis(df_enriched)
    analyzer.task_3_1_pattern_analysis()
    analyzer.task_3_2_correlation_insights()
    
    visualizer = Visualization(df_enriched)
    visualizer.task_4_1_visualizations()
    visualizer.task_4_2_generate_report()
    
    print("\n" + "="*80)
    print("EXECUTION COMPLETED SUCCESSFULLY! ✓".center(80))
    print("="*80)
    print("\nOutput Files Generated:")
    print("  📊 Visualizations (6 high-resolution PNG files)")
    print("  📄 RAILWAY_ANALYSIS_REPORT.txt (Comprehensive report)")
    print("\nAll files are ready for presentation to stakeholders!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
