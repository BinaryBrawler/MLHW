#author: robert hart
#name: k-means clustering using manhattan distance

import os
import numpy as np

def calculate_manhattan_distance(vector_size, dataset, centroids):
    manhattan_distances = []
    for i in range(len(dataset)):
        temp_array = []
        #for every centroid
        for j in range(len(centroids)):
            temp_distance = 0
            #for every dimension
            for k in range(vector_size):
                single_dimension_distance = abs(dataset[i][k] - centroids[j][k])
                temp_distance = temp_distance + single_dimension_distance
            temp_array.append(temp_distance)
        manhattan_distances.append(temp_array)
    return manhattan_distances

def assign_clusters(num_centroids, manhattan_distances):
    cluster_map_working = []
    cluster_map_final = []
    for i in range(len(manhattan_distances)):
        shortest_distance = min(manhattan_distances[i])
        closest_cluster = manhattan_distances[i].index(shortest_distance) + 1
        cluster_map_working.append(closest_cluster)
    for i in range(num_centroids):
        centroids_temp = []
        for j in range(len(cluster_map_working)):
            if cluster_map_working[j] == i+1:
                centroids_temp.append(j)
        cluster_map_final.append(centroids_temp)
    return cluster_map_final

def update_clusters(vector_size, centroids, cluster_map, dataset):
    for i in range(len(cluster_map)):
        new_centroid = np.zeros([vector_size,1]).T
        new_centroid = new_centroid.flatten()
        for j in cluster_map[i]:
            new_centroid = (np.array(dataset[j]) + new_centroid)
        new_centroid = (1/len(cluster_map[i])) * new_centroid
        centroids[i] = new_centroid.tolist()
    return centroids

def iterate(vector_size, num_centroids, dataset, centroids):
    manhattan_distances = calculate_manhattan_distance(vector_size, dataset, centroids)
    cluster_map = assign_clusters(num_centroids, manhattan_distances)
    centroids = update_clusters(vector_size, centroids, cluster_map, dataset)
    return centroids

def kmeans(dataset, centroids):
    kmeans_info = []
    dataset_size = len(dataset)
    vector_size = len(dataset[0])
    num_centroids = len(centroids)
    centroids_previous = list(centroids)
    centroids_current = iterate(vector_size, num_centroids, dataset, list(centroids))
    count = 1

    while True:
        equality_array = np.allclose(np.array(centroids_previous, dtype=float).flatten(), np.array(centroids_current, dtype=float).flatten(), rtol=1e-06, atol=1e-08)
        if equality_array == True:
            break
        else:   
            count = count + 1
            #print(equality_array)
            equality_array
            temp = centroids_current
            centroids_current = iterate(vector_size, num_centroids, dataset, temp)
            centroids_previous = temp
        

    kmeans_info.append(centroids_current)
    kmeans_info.append(count)

    return kmeans_info

def main():
    #the following must be set by the user
    dataset = [[1,2], [2,2], [4,4], [5,4], [5,5]]
    centroids = ((1,2), (2,2))

    #print initial dataset, initial centroids, new centroids, number of iterations
    kmeans_info = kmeans(dataset, centroids)

    for i in range(len(kmeans_info[0])):
        kmeans_info[0][i] = tuple(kmeans_info[0][i])
    
    kmeans_info[0] = tuple(kmeans_info[0])

    print(
        f'''
        Dataset: {dataset}

        Original centroids: {centroids}
        Final centroids: {tuple(kmeans_info[0])}
        Number of iterations: {kmeans_info[1]}
        '''
    )

main()