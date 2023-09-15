import numpy as np


def gen_RGB_list(n: int) -> list:
    """
    Generate a list of RGB colors with length n.
    """
    if n <= 0 or n > 256 ** 3:
        raise ValueError('n must be in range [1, 256**3]')
    rgb_list = []
    for i in range(n):
        rgb = np.random.randint(0, 256, size=3)
        if i > 0:
            rgb_old = rgb_list[i - 1]
            # avoid similar colors, angle > pi/5
            while np.arccos(np.dot(rgb_old, rgb) / (np.linalg.norm(rgb_old) * np.linalg.norm(rgb))) < np.pi / 5:
                rgb = np.random.randint(0, 256, size=3)
        rgb_list.append(rgb)
    return rgb_list
