import numpy as np


def subtract_points(p1, p2):
    return np.array(p1) - np.array(p2)


def vector_length(v):
    return np.linalg.norm(v)


def normalize_vector(v):
    norm = vector_length(v)
    if norm == 0:
        return np.zeros_like(v)
    return v / norm


def midpoint(p1, p2):
    return (np.array(p1) + np.array(p2)) / 2
