import pymysql
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
from numpy.linalg import norm
import sys
import math
import getpass


def db_to_df(user, password, host, database, city):
    csv_file_path = './location.csv'
    db_opts = {
        'user': user,
        'password': password,
        'host': host,
        'database': database
    }
    db = pymysql.connect(**db_opts)
    cur = db.cursor()
    sql = 'select latitude, longitude, review_count from business where city=' + '"' + city + '"'
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        db.close()

    if rows:
        headers = list()
        for header in cur.description:
            headers.append(header[0])
        fp = open(csv_file_path, 'w')
        my_file = csv.writer(fp)
        my_file.writerow(headers)
        my_file.writerows(rows)
        fp.close()
    else:
        sys.exit('no rows found for query: {}'.format(sql))

    df = pd.read_csv(csv_file_path)
    df_location = df.iloc[:, 0:2]
    df = df[(np.abs(zscore(df_location)) < 0.8).all(axis=1)]
    category = pd.qcut(df['review_count'], 3, labels=['low counts', 'mid counts', 'high counts']).to_frame()
    category.columns = ['review_count_level']
    df_new = pd.concat([df, category], axis=1)
    return df_new


class K_means:

    def __init__(self, k=12, tolerence=0.1, max_iteration=500):
        self.k = k
        self.tolerence = tolerence
        self.max_iteration = max_iteration
        self.centroids = []
        self.clusters = [[] for i in range(self.k)]

    def Euclidean_distance(self, p1, p2):
        return norm(p1 - p2)

    def fit(self, df):
        arr = df.values
        # Initialize the centroids to the first k data points
        self.centroids = [arr[i] for i in range(self.k)]
        previous_total_distance = math.inf
        print("please wait for convergence:")
        for i in range(self.max_iteration):
            new_total_distance = 0
            # Generate clusters based on k centroids
            for j in arr:
                distances_to_centroids = [norm(j - centroid) for centroid in self.centroids]
                min_distance = min(distances_to_centroids)
                new_total_distance += min_distance
                nearest_centroid_index = distances_to_centroids.index(min_distance)
                self.clusters[nearest_centroid_index].append(j)
            # Compute new centroid for each cluster
            self.centroids = [np.average(cluster, axis=0) for cluster in self.clusters]
            if i > 0:
                if np.abs(new_total_distance - previous_total_distance) < self.tolerence:
                    break
            previous_total_distance = new_total_distance
            print("current loss: ", previous_total_distance)

    def visualize(self):
        df_centroid = pd.DataFrame.from_records(self.centroids, columns=['latitude', 'longitude'])
        df_data = []
        for i in range(len(self.clusters)):
            df = pd.DataFrame.from_records(self.clusters[i], columns=['latitude', 'longitude'])
            df['cluster'] = i
            df_data.append(df)
        df = pd.concat(df_data).reset_index(drop=True)
        sns.lmplot(x='longitude',
                   y='latitude',
                   hue='cluster',
                   data=df,
                   fit_reg=False,
                   scatter_kws={"s": 10})
        plt.show()


while 1:
    try:
        u = input("please enter your user name of MySQL:")
        h = input("please enter your host name of MySQL:")
        p = getpass.getpass(prompt = "please enter your password for user " + u + ":")
        db = input("please enter the database name which contains the table business:")
        c = input("please enter the city name you'd like to analyze:")
        df_new = db_to_df(u, p, h, db, c)

        # sns.set(font_scale=1.2)
        # sns.lmplot(x='longitude',
        #            y='latitude',
        #            hue='review_count_level',
        #            data=df_new, fit_reg=False,
        #            scatter_kws={"s": 10})
        # plt.suptitle('Yelp view counts vs location')
        # plt.show()

        km = K_means()
        km.fit(df_new[['latitude', 'longitude']])
        km.visualize()
        break
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("something went wrong, please try again!", sys.exc_info()[0])
