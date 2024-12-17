# SimpleSpeak
# **IMU-Based Speech Command Classification Using Jaw Motion**

### **Overview**  
The ability to interact with devices using speech commands has transformed modern technology, powering innovations in voice assistants, smart devices, and hands-free systems. However, traditional audio-based speech recognition systems face challenges such as environmental noise, privacy concerns, and limited accessibility for individuals with speech impairments.  

This project introduces a **motion-based alternative** for speech command recognition by leveraging **Inertial Measurement Unit (IMU)** sensors to analyze jaw movements during speech. By capturing **accelerometer** and **gyroscope** data from an IMU sensor placed on the lower jaw, the system accurately classifies spoken commands without relying on audio. This approach ensures a **noise-resilient**, **privacy-conscious**, and **inclusive** solution for real-time speech command recognition.

---

### **Key Features**  
- **Noise Robustness**: Works effectively in loud environments where audio-based systems fail.  
- **Privacy-Focused**: Uses motion data instead of sensitive audio recordings.  
- **Accessibility**: Provides an alternative communication method for individuals with speech impairments.  
- **Real-Time Predictions**: Processes IMU data and triggers actions seamlessly on mobile devices.  
- **Wearable Integration**: Demonstrates potential for hands-free control of devices like smartphones, smart home systems, and assistive tools.  

---

### **System Workflow**  

1. **Data Collection**  
   - IMU (accelerometer and gyroscope) sensor placed on the lower jaw captures motion data during speech.  
   - Commands such as *"Call"*, *"Unlock"*, *"End"*, and *"Pick Up Call"* are recorded with corresponding jaw movements.  

2. **Data Preprocessing**  
   - Filtering and visualization of accelerometer data to ensure quality.  
   - Extraction of key features such as mean, median, standard deviation, and syllable count using peak detection.  

3. **Feature Engineering**  
   - Selected features include:
     - Statistical metrics: Mean, Median, Standard Deviation  
     - Syllable count (using peak detection with `scipy.find_peaks()`)  
     - Additional candidates (e.g., FFT features, spectral energy) were evaluated but not included in the final model.  

4. **Machine Learning Model**  
   - **Random Forest Classifier** is used for command classification due to its robustness, ability to handle small datasets, and real-time prediction capabilities.  
   - The model achieves an accuracy of **88%**.  

5. **Real-Time Prediction and ADB Integration**  
   - The trained model processes real-time IMU data to classify speech commands.  
   - Using **Android Debug Bridge (ADB)**, the system seamlessly triggers actions on a connected mobile device.  
     - Example: Predicting "Unlock" sends an ADB command to simulate a swipe gesture and unlock the phone.  

---

### **Challenges and Solutions**  

1. **Overfitting During Initial Training**  
   - **Issue**: Initial data collection (30 samples in one sitting) led to overfitting when the IMU was reattached.  
   - **Solution**: Data was collected in smaller batches (5 samples at a time), with IMU detachment and reattachment between batches to improve generalization.  

2. **Placement of IMU Sensor**  
   - **Issue**: Data collected from the TMJ (Temporomandibular Joint) was not distinct enough for classification.  
   - **Solution**: IMU placement was shifted to the **lower jaw**, yielding clearer and more distinguishable motion data.  

3. **Feature Selection**  
   - Multiple features (e.g., FFT dominant frequency, spectral energy) were tested before selecting the optimal feature set for accuracy and performance.

---

### **Technologies Used**  
- **Hardware**: IMU sensor (Accelerometer and Gyroscope)  
- **Programming Languages**: Python  
- **Libraries**:  
   - `scipy` - Signal processing (e.g., filtering, peak detection)  
   - `pandas`/`numpy` - Data analysis and processing  
   - `sklearn` - Machine learning (Random Forest Classifier)  
- **Tools**:  
   - **Android Debug Bridge (ADB)** for real-time device control  
   - **Matplotlib** for data visualization  

---

### **Real-Time Demo**  
Watch the end-to-end demonstration of the project here:  
https://drive.google.com/file/d/1g4QbBxXHoueTJju_Ub60Bt_T03qUPyH6/view?usp=share_link

---

### **Future Scope**  
- Integrating the system into wearable devices for hands-free control.  
- Expanding the command set for broader applications.  
- Improving model robustness with larger datasets and advanced algorithms like deep learning.  

---

### **Contributors**  
- Shivani Anilkumar
- Khushi Gandhi
- Manav Manoj Dhelia 
---

### **Acknowledgments**  
Special thanks to the University of Massachusetts, Amherst for providing resources and support for this project.  
