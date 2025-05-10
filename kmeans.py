import numpy as np
import random


def kmeans(points, k=3, max_iters=100):
    if not points:
        return [], []
    points_np = np.array(points)
    np.random.shuffle(points_np)
    centroids = points_np[:k].tolist()

    for _ in range(max_iters):
        clusters = [[] for _ in range(k)]
        for point in points:
            distances = [np.linalg.norm(np.array(point) - np.array(c)) for c in centroids]
            cluster_idx = np.argmin(distances)
            clusters[cluster_idx].append(point)

        new_centroids = []
        for cluster in clusters:
            if cluster:
                new_c = np.mean(cluster, axis=0).astype(int).tolist()
                new_centroids.append(new_c)
            else:
                new_centroids.append(centroids[len(new_centroids)])

        if np.array_equal(new_centroids, centroids):
            break
        centroids = new_centroids
    return clusters, centroids