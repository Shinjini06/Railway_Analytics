# PROJECT OVERVIEW

## Railway Data Engineering Project

Comprehensive analysis of 11,113 railway operational records using Python data engineering techniques. All 4 levels completed: Data Exploration, Transformation, Advanced Analysis, and Visualization with Professional Reporting.

## Dataset Details

- Total Records: 11,113
- Source Stations: 921
- Destination Stations: 924
- Unique Trains: 11,113
- Data Quality: Zero missing values, zero duplicates

## Key Findings

| Metric | Value |
|--------|-------|
| Peak Operating Day | Friday (1,471 trains) |
| Weekday Operations | 74.15% |
| Weekend Operations | 25.85% |
| Top Station Hub | CST-MUMBAI (513 departures) |
| Busiest Route | CHENNAI BEACH to TAMBARAM (137 trains) |
| Train Type Focus | 99.87% Inter-city, 0.13% Local |

## Levels Completed

Level 1: Data Exploration and Cleaning
- Data inspection and validation
- Missing value analysis
- Station name standardization

Level 2: Data Transformation and Aggregation
- Filtering by specific criteria (Saturday trains, specific stations)
- Grouping by source station and day of week
- Feature enrichment (Weekday/Weekend categorization, Local/Inter-city classification)

Level 3: Advanced Data Analysis
- Pattern analysis by day of week
- Peak day identification
- Route pair analysis
- Business insights and recommendations

Level 4: Data Visualization and Reporting
- 6 professional visualizations (PNG format)
- Comprehensive text report
- Strategic recommendations

## Visualizations

1. viz_1_trains_by_day.png - Train distribution by day of week
2. viz_2_top_source_stations.png - Top 15 source stations
3. viz_3_top_destination_stations.png - Top 15 destination stations
4. viz_4_weekday_weekend.png - Weekday vs weekend comparison
5. viz_5_train_types.png - Local vs inter-city distribution
6. viz_6_heatmap_routes.png - Source-destination traffic heatmap

## Technologies Used

- Python 3.7+
- Pandas (Data manipulation)
- NumPy (Numerical operations)
- Matplotlib (Visualization)
- Seaborn (Advanced visualization)

## How to Run

Install dependencies:
```bash
pip install pandas numpy matplotlib seaborn
```

Execute analysis:
```bash
python railway_data_analysis.py
```

Output files generated:
- 6 PNG visualization files
- RAILWAY_ANALYSIS_REPORT.txt (comprehensive report)

## Project Structure

```
Railway_Data_Engineering_Project/
├── railway_data_analysis.py
├── Railway_info.csv
├── RAILWAY_ANALYSIS_REPORT.txt
├── PROJECT_OVERVIEW.md
├── viz_1_trains_by_day.png
├── viz_2_top_source_stations.png
├── viz_3_top_destination_stations.png
├── viz_4_weekday_weekend.png
├── viz_5_train_types.png
└── viz_6_heatmap_routes.png
```

## Code Quality

- Object-oriented design with 5 modular classes
- Professional documentation and comments
- Error handling and data validation
- Production-ready code structure

## Author

Shinjini Pal
B.Tech CSE (3rd Year) - Jain Global Campus, Bangalore

GitHub: https://github.com/Shinjini06
LinkedIn: https://linkedin.com/in/shinjini-pal-120086220
Email: srijasaha1224@gmail.com
