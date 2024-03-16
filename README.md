## Dashboard: Historical Analysis of Wildfires in the United States

Wildfires are a global phenomenon that lead to significant losses, not only in terms of money but also in vegetation and wildlife. The dashboard aims to provide historical data and insights regarding wildfires in the USA, offering a comprehensive resource for understanding past trends in wildfire behavior.

Our dashboard is structured into two pages. The plots can be filtered using the control settings available:

- Slider: Filters the year from 1992 to 2009.
- Dropdowns:
  - Select one of the 52 states of America or display all of them at the same time.
  - Select one fire size class from A to G (low to high) or display all of them together.

----------------------------

### Page 1: Understanding Wildfires - General Overview

Wildfires are a significant ecological and economic concern in the United States. In this section, the dashboard provides a comprehensive overview of historical wildfire data, offering insights into the frequency, extent, and distribution of wildfires across different states and over time. This page contains four plots and focuses on answering the following questions:

#### Questions: 

- What is the total number of wildfire incidents in a given range of years with a particular size in specific state(s)?
- Which state is most affected by wildfires in terms of area consumed?
- What is the frequency of wildfire incidents in a given range of years with a particular size in specific state(s)?
- What is the total area affected by wildfire incidents in a given range of years with a particular size in specific state(s)?

#### Plots: 

- Map Plot: This plot visually represents the geographic distribution of wildfires across USA states. It utilizes geospatial data to display each state's area affected by wildfires, with color gradients indicating varying levels of impact.
- Bar Plot: The horizontal bar plot displays the top ten states with the largest number of acres burned.
- Count Label: For simplicity and ease of interpretation, count labels are used to show cumulative figures without requiring the user to calculate on their own. This is used to display the total number of wildfire incidents and total areas affected by wildfires.
- Area Plot: This chart depicts the intensity of wildfires in terms of the area affected over a specified time period. By visualizing the fluctuation in wildfire intensity over time, viewers can gain a better understanding of historical trends and variations in wildfire activity.

---------------------------------

### Page 2: Discovering the Causes

In this section of the dashboard, we have four plots. We start by analyzing all fire causes, then we analyze their frequency by cause and fire size class. Next, we classify the causes into two main groups: human-caused and lightning-caused fires to make comparisons about the number of fires by month and regional area. We conclude our analysis with the total acres burned for both groups and regional areas.

#### Questions: 

- What are the most common causes of wildfires and their intensity?
- What is the trend of fires for the most common causes: human-caused and lightning-caused?
- What is the number of fires for the most common causes: human-caused and lightning-caused by region?
- What is the total acres burned for the most common causes: human-caused and lightning-caused by region?

#### Plots: 

- Correlation Chart: This explores the relationship between the total area affected by wildfires and their various sources. By analyzing correlations between wildfire causes and the extent of their impact, this chart aims to provide insights that can inform strategies for mitigating wildfire damage.
- Line Chart: This illustrates the monthly trend of the number of wildfire incidents for human-caused and lightning-caused fires. This visual representation enables viewers to track changes in the frequency of wildfires over time.
- Stacked Bar Chart: This illustrates the number of wildfire incidents for human-caused and lightning-caused fires by regional area. This visual representation enables viewers to track changes in both the frequency of wildfires and the extent of their impact over time.

----------------------

#### Initial Sketch 

- The map shown in the sketch corresponds to the python code in [map.py](https://github.com/andrewsarracini/DATA551_FireAnalysis/blob/main/map.py)
- This is sketch is an early idea of how we envison our final product, preserved for posterity
![Image](dashboard_sketch.png)

--------------------

#### Final Dashboard Screenshots
  
![Image](FireAnalysis_Page1.png) 
![Image](FireAnalysis_Page2.png) 
