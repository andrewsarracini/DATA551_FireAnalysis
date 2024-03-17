## Dashboard: Historical Wildfires in USA

Wildfires are a global phenomenon that leads to significant losses not only costly in money but also in terms of vegetation and wildlife. The dashboard aims to provide historical data and insights regarding wildfires in the USA, offering a comprehensive resource for understanding past trends on wildfire behavior.

Link to the dashboard : https://wildfireanalysis.onrender.com 

Our dashboard focuses on answering the below questions:
1. Are there any spacial cluster in wildfire incidents and how it is related to the size of the fire and Year of occurance?
2. What is the total number of wildfire incidents in a range of year with particular size in particular state(s)?
3. What is the total area affected by wildfire incidents in range of year with particular size in particular state(s)?
4. Which state is most affected by wildfires in terms of frequency and area consumed? 
5. What are the most common causes of wildfires, both per state and across the country? 
6. What are the top and bottom states in terms of fast and efficient containment of wildfires?
7. Are there any mitigating or aggravating factors that are contributing to the result? 
8. What factors might lead to faster containment of wildfires? 

We are planning to have 8 plots, 2 count labels and 3 filters.

##### Map Plot:

The map plot will visually represent the geographic distribution of wildfires across USA states. It will utilize geospatial data to display each state's area affected by wildfires, with color gradients indicating varying levels of impact.

##### Count Label:

For simplicity and ease of Interpretation, count labels are used to show cumulative figure without letting the user to calculate on their own. This is used to show total number of wildfire incidents and total areas affected by wildfire.

##### Line chart:
This will illustrate the trend of wildfire incidents and the total area affected over a specified time period. This visual representation will enable viewers to track changes in both the frequency of wildfires and the extent of their impact over time.


##### Histogram plot:
This will showcase the distribution of containment duration for wildfires across different states. By presenting the average duration taken to contain wildfires, viewers can discern which states have been more effective in containing wildfires and identify potential areas for improvement.


##### Correlation chart:
This will explore the relationship between the total area affected by wildfires and their various sources. By analyzing correlations between wildfire causes and the extent of their impact, this chart aims to provide insights that can inform strategies for mitigating wildfire damage.


##### Area plot
This chart will depict the intensity of wildfires in terms of the area affected over a specified time period. By visualizing the fluctuation in wildfire intensity over time, viewers can gain a better understanding of the historical trends and variations in wildfire activity.

##### Initial Sketch 
- The map shown in the sketch corresponds to the python code in [map.py](https://github.com/andrewsarracini/DATA551_FireAnalysis/blob/main/map.py)
- This is sketch is an early idea of how we envison our final product, preserved for posterity
![Image](dashboard_sketch.png)

##### Final Dashboard Screenshots
- Final Screenshots of our Dashboard
![Image](FireAnalysis_Page1.png) 
![Image](FireAnalysis_Page2.png) 
