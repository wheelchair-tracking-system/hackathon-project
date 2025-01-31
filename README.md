# 🏥 **Real-Time Wheelchair Tracking System**  

### 📌 **Overview**  
This project is a **live wheelchair tracking system** designed for **hospital management** to ensure the efficient allocation and availability of wheelchairs. The system helps hospital staff locate wheelchairs in real time, track their movement across floors, and manage emergency wheelchair requests effectively.  

It was initially developed as a prototype during the **Healthcare Hackathon at JECRC University** to address the problem of **wheelchair mismanagement** in hospitals. The system enables **staff to dispense, request, and track wheelchairs** seamlessly via an **admin panel**.  

---

## ⚙️ **Features**  
✔️ **Live GPS-based wheelchair tracking**  
✔️ **Emergency wheelchair request system**  
✔️ **Admin panel for monitoring wheelchair availability and location**  
✔️ **Maintenance request system**  
✔️ **User-friendly web interface for hospital staff**  

---

## 🛠 **Technology Stack**  

### **Frontend:**  
- **HTML, CSS, JavaScript** – For building a responsive and interactive UI  

### **Backend:**  
- **Flask (Python)** – Handles API requests and server-side logic  

### **Hardware:**  
- **Arduino Uno R3** – Microcontroller to interface with the GPS module  
- **Neo 6M V2 GPS Module** – Provides accurate **latitude & longitude** coordinates of the wheelchair  

### **Real-time Updates & Data Flow:**  
1. The **GPS module** fetches real-time location (latitude & longitude) of the wheelchair.  
2. The **Arduino Uno R3** processes the data and sends it to the server.  
3. The **backend (Flask)** stores this data in the database.  
4. The **admin panel** fetches the latest wheelchair locations and displays them on a map.  
5. Emergency requests and maintenance issues can be **monitored & managed via the dashboard**.  

---

## 🚀 **Future Enhancements**  
🔹 **Wi-Fi-based real-time updates instead of wired data transfer** 
🔹 **RFID-based tracking** 
🔹 **Integration with hospital management software (HMS)**  
🔹 **Live notifications for emergency & maintenance requests**  
🔹 **Mobile app support for hospital staff**  
🔹 **Automated alerts when a wheelchair is inactive for too long**   

---

## 🏆 **Acknowledgments**  
🚀 **Developed during the Healthcare Hackathon at JECRC University**  
💡 **Thanks to my amazing team for the collaboration!**  
