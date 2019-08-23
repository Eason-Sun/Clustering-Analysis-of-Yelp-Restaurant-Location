# Clustering-analysis-of-yelp-restaurant-location

## Dataset:
https://www.yelp.ca/dataset/challenge

## Motivation:
Unsupervised learning algorithm becomes really useful when it comes to massive unlabeled raw data. As a result, it is widely used for data mining to reveal unknown patterns. In this particular application, our goal is to generate clusters that well represent urban commercial areas, which provides references for new business owners to have a comprehensive understanding of urban layout so that they could make wise decision of choosing the proper locations.

## Implementation:
Apply K-Means Clustering on location data (Latitude, Longitude) from business table. The loss function we chose for K-Means Clustering is the total sum of Euclidean distances from samples to their centroids. Users are free to fine tune hyperparameters such as:

1) Number of centroids k (default k = 12);  
2) Maximum number of iterations max_iteration (default max_iteration = 500);  
3) Minimum decrement in loss function tolerance (default tolerance = 0.1)  

The algorithm converges when maximum number of iterations are reached, or the gain of the loss function is negligible. Consequently, the descriptive power of k centroids is maximized, in other words, they are optimal representations of all datapoints
Use visualize () to show to K-Means Clustering results:

## Visualization:

![ECE 656 Project Report](https://user-images.githubusercontent.com/29167705/63561120-beadc880-c526-11e9-8f27-f67251c6eb66.jpg)

As the above figure shown, the city Las Vegas is now divided into 12 commercial districts represented by corresponding colours. It can be clearly observed that business owners tend to locate and exploit their properties near the main streets and street corners.

![Capture](https://user-images.githubusercontent.com/29167705/63561197-0e8c8f80-c527-11e9-97d7-2c2969c8b28b.JPG)

The left figure illustrates the relationship between review counts and their locations. Data are binned equally into 3 ranks (high counts: green; mid counts: orange; low counts: blue). As we can see, the left vertical street is the busiest. On the corresponding google map, it turns out that there are full of casinos on that street.
