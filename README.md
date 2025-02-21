# **VisiTex** 🎥✍️  
### **Detection & Segmentation with Text-Based Classes**  

**VisiTex** allows you to process videos using AI-powered **detection** and **segmentation**. Simply upload a video, specify object classes as a comma-separated list, and get results in seconds.  

---

## **🚀 Installation**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/mubeen-afzal/VisiTex
cd VisiTex
```

### **2. Set Up the Environment**  

#### **Option 1: Using Conda (Recommended)**  
```bash
conda create -n obj_tracker python==3.11
conda activate obj_tracker
```

#### **Option 2: Using a Python Virtual Environment**  
```bash
python -m venv obj_tracker
source obj_tracker/bin/activate  # Mac/Linux
obj_tracker\Scripts\activate     # Windows
```

### **3. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4. Run the Application**  
```bash
python app.py
```
**Note:** The first run may take longer as it downloads the necessary models.  

### **5. Access the Web Interface**  
Once running, open your browser and go to:  
**[http://127.0.0.1:7860](http://127.0.0.1:7860)**  

---

## **📌 How to Use**  

1. **Upload a video** from your local directory.  
2. **Select an operation:**  
   - **Track** – Detect and track objects across frames.  
   - **Segment** – Perform object segmentation.  
3. **Enter object classes** as a comma-separated list (e.g., `car, ball, person`).  
4. Click **Submit** to process the video.  
5. The processed video will appear on the right, and you can **download it** if needed.  

---

## **🔧 Troubleshooting**  
- **App not opening?** Ensure the environment is activated and `python app.py` is running.  
- **Missing dependencies?** Run `pip install -r requirements.txt` again.  
- **Still facing issues?** Open an issue in the repository.  

---