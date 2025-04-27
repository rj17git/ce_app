import cv2
from skimage import measure
from skimage.measure import regionprops
import pandas as pd
import numpy as np

def preprocess_image(image, cell=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    if not cell:
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.dilate(binary, kernel, iterations=1)
    
    inverted = cv2.bitwise_not(binary)
    labeled = measure.label(inverted, connectivity=1)

    return labeled


def analyze_cell(image, selected_cell_id):
    colored_image = image.copy()
    labeled = preprocess_image(image, cell=True)
    props = regionprops(labeled)

    

    for prop in props:
        if prop.label == int(selected_cell_id):
            for x, y in prop.coords:
                colored_image[x, y] = [255, 0, 0]
            break
    
    return colored_image

def analyze_image(image, image_name, min_circularity, max_circularity, pixel_horizontal_value, pixel_vertical_value):
    labeled = preprocess_image(image)
    props = regionprops(labeled)

    cell_data = []
    for prop in props:
        if prop.area > 20:
            minr, minc, maxr, maxc = prop.bbox
            area = prop.area
            perimeter = prop.perimeter
            circularity = (4 * np.pi * area) / (perimeter**2)
            ratio = (maxc - minc)/(maxr - minr)
            cell_data.append({
                "image_name" : image_name,
                "cell_id" : prop.label,
                "area" : area,
                "perimeter" : perimeter,
                "circularity" : circularity,
                "ratio" : ratio,
                "bbox" : (minr, minc, maxr, maxc)
            })

    dataset_cell = pd.DataFrame(cell_data)
    available_cell = dataset_cell.query(f"0.4 < circularity")
    hexagonal_dataset = dataset_cell.query(f"{min_circularity} < circularity < {max_circularity}")
    total_cells = available_cell.shape[0]
    hexagonal_cells = hexagonal_dataset.shape[0]

    density = total_cells / (pixel_vertical_value*labeled.shape[0]*pixel_horizontal_value*labeled.shape[1])
    CV = (available_cell["area"].std()) / (available_cell["area"].mean()) * 100

    stats = {
        "image_name" : image_name,
        "N_hexagonal_cells" : hexagonal_cells,
        "N_total_cells" : total_cells,
        "hexagonality_coeff" : (round(hexagonal_cells*100 / total_cells, 2)),
        "CV" : round(CV, 2),
        "density" : round(density, 2)
    }

    return available_cell, hexagonal_dataset, stats, labeled