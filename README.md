# spheroid_morpho_ML

This project aims to **segment spheroid images**, extract their **morphological properties**, and use **MIIC algorithm** to study the relative importance of the morpholigical features before using **machine learning** to **classify spheroids based on viability** and **predict dose-response curves**.  

## 📂 Project Structure  

### **1️⃣ Image Segmentation** (`segmentation_images/`)  
This folder contains **`spheroid_segmentation.py`** to extract **spheroid morphological properties** from images.  
📸 **Example images** are included for testing in `segmentation_images/data_segmentation`.

### **2️⃣ MIIC**


### **3️⃣ Classification and Prediction** (`machine_learning_classification/`)  
This folder contains **notebooks for spheroid classification**:  
- **`1_data_processing_spheroids_morpho.ipynb`**: Data preprocessing to structure spheroid morphological properties.  
- **`2_data_exploration_spheroids_morpho.ipynb`**: Data visualization.  
- **`3_machine_learning_spheroids_morpho.ipynb`**: Machine learning implementation to **classify spheroids based on viability** and **predict dose-response curves**.  

---

## ⚙️ Installation  

### **1️⃣ Prerequisites**  
- Tested with **Python 3.12.7**  
- **Dependencies** (install with pip):  
  ```bash
  pip install -r requirements.txt


### **🚀 Usage**
1️⃣ Image Segmentation
Run the script to script **`spheroid_segmentation.py`**. The masks, segented images and extracted properties are saved in the folder `segmentation_images/output`.

2️⃣ MIIC

3️⃣ Spheroid Classification
 - Run `1_data_processing_spheroids_morpho.ipynb` to preprocess data
 - Run `2_data_exploration_spheroids_morpho.ipynb` to visualize data
 - Run `3_machine_learning_spheroids_morpho.ipynb` to train and test the model
    
## 👥 Contributors
  - **Caroline Parent**  
  - **Tiziana Tocci**  
  - **Hasti Honari**  
