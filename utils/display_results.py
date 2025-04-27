import streamlit as st
from utils.image_loader import get_image
from utils.analyze_image import analyze_cell, analyze_image

def sidebar_inputs():
    st.sidebar.title("Corneal Endothelium Analysis")
    source = st.sidebar.radio("Image Source", ["From directory", "Uploaded image"])
    min_circularity, max_circularity = st.sidebar.slider("Min Circularity", 0.5, 1.0, (0.87, 0.95), 0.01)
    pixel_vertical_size = st.sidebar.number_input("Vertical Pixel Size (mm)", value=0.001075)
    pixel_horizontal_size = st.sidebar.number_input("Horizontal Pixel Size (mm)", value=0.000884)
    
    return source, min_circularity, max_circularity, pixel_vertical_size, pixel_horizontal_size


def display_results(image, image_name, available_dataset, hexagonal_dataset, stats):
           # Organisation in 2 columns
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption=image_name, use_container_width=False)
    with col2:
        st.subheader("Morphometric parameters")
        st.json(stats)

    st.subheader("Detailed Data per Cell")

    selected_index = st.number_input(f"Select cell ID to highlight (between {0} and {len(available_dataset)-1})", min_value=0, max_value=len(available_dataset)-1, step=1)

    if 0 <= selected_index < len(available_dataset):
        selected_cell = available_dataset.iloc[selected_index]
        selected_cell_id = available_dataset.iloc[selected_index]["cell_id"]
        colored_image = analyze_cell(image, selected_cell_id)
    
        # Organisation in 2 columns
    col1, col2 = st.columns(2)

    with col1:
        st.image(colored_image, caption="Highlighted cell", use_container_width=True)

    with col2:
        st.markdown(f"### Cell characteristics")

        st.write(f"**Area:** {selected_cell['area']:.2f} pixels")
        st.write(f"**Perimeter:** {selected_cell['perimeter']:.2f} pixels")
        st.write(f"**Circularity:** {selected_cell['circularity']:.3f}")
        st.write(f"**Ratio (W/H):** {selected_cell['ratio']:.3f}")


def postprocessing_view():
    source, min_circularity, max_circularity, pixel_vertical_size, pixel_horizontal_size = sidebar_inputs()
    image, image_name = get_image(source)

    if image is not None:
        available_cell, hexagonal_dataset, stats, labeled = analyze_image(image, image_name, min_circularity, max_circularity, pixel_vertical_size, pixel_horizontal_size)
        display_results(image, image_name, available_cell, hexagonal_dataset, stats)
    else:
        st.info("Choose or upload an image")