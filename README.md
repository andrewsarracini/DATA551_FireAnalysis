## Dashboard: Historical Wildfires in USA

Wildfires are a global phenomenon that leads to significant losses not only costly in money but also in terms of vegetation and wildlife. The dashboard aims to provide historical data and insights regarding wildfires in the USA, offering a comprehensive resource for understanding past trends on wildfire behavior.

Link to the dashboard : https://wildfireanalysis.onrender.com 

Our dashboard is structured into two pages. The plots can be filtered using the control settings available:

- Slider: Filters the year from 1992 to 2009.
- Dropdowns:
  - Select one of the 52 states of America or display all of them at the same time.
  - Select one fire size class from A to G (low to high) or display all of them together.
- Tooltip: this feature allows the user to hover over the plots, and count labels will be displayed to show cumulative figures without requiring the user to calculate them manually. This feature is used to show the total number of wildfire incidents and the total area affected by wildfires.
  
It focuses on answering the below questions:

1. Are there any spacial cluster in wildfire incidents and how it is related to the size of the fire and Year of occurance?
2. What is the total number of wildfire incidents in a range of year with particular size in particular state(s)?
3. What is the total area affected by wildfire incidents in range of year with particular size in particular state(s)?
4. Which state is most affected by wildfires in terms of frequency and area consumed? 
5. What is the trend of fires for the most common causes: human-caused and lightning-caused?
6. What is the number of fires for the most common causes: human-caused and lightning-caused by region?
7. What is the total acres burned for the most common causes: human-caused and lightning-caused by region?

### Plots Page 1

##### Map Plot:
The map plot will visually represent the geographic distribution of wildfires across USA states. It will utilize geospatial data to display each state's area affected by wildfires, with color gradients indicating varying levels of impact.

##### Horizontal Bar plot:
This plot displays the top 10 states affected by fires and the total acres burned.

##### Area Plot
This chart will depict the intensity of wildfires in terms of the area affected over a specified time period. By visualizing the fluctuation in wildfire intensity over time, viewers can gain a better understanding of the historical trends and variations in wildfire activity.

### Plots Page 2

##### Heatmap Chart:
This explores the relationship between the total area affected by wildfires and their various sources. By analyzing correlations between wildfire causes and the extent of their impact, this chart aims to provide insights that can inform strategies for mitigating wildfire damage.

##### Line Chart:
This illustrates the monthly trend of the number of wildfire incidents for human-caused and lightning-caused fires. This visual representation enables viewers to track changes in the frequency of wildfires over time.

##### Stacked Bar Chart:
This illustrates the number of wildfire incidents for human-caused and lightning-caused fires by regional area. This visual representation enables viewers to track changes in both the frequency of wildfires and the extent of their impact over time.


#### Initial Sketch 
- The map shown in the sketch corresponds to the python code in [map.py](https://github.com/andrewsarracini/DATA551_FireAnalysis/blob/main/map.py)
- This is sketch is an early idea of how we envison our final product, preserved for posterity.
  
![Image](dashboard_sketch.png)     

#### Final Dashboard Screenshots
![Image](FireAnalysis_Page1.png) 
![Image](FireAnalysis_Page2.png) 
