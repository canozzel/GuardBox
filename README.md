# GuardBox – Smart Cargo Security System

**GuardBox** is an IoT-based smart lockbox system designed to prevent package theft by securing deliveries left outside homes. It intelligently detects actual package placement using a load cell, locks only when a package is present, and provides live updates across all user platforms.

Developed as part of the “Special Topics in Computer Engineering (CEN309)” course at Maltepe University, GuardBox is still actively maintained and improved.

---

## 🔐 Key Features

- 📦 **Package Detection** – Uses a load cell to detect the presence of real packages
- 🔒 **Smart Locking** – Automatically locks when a package is placed
- ⚠️ **Tamper Detection** – Vibration sensor detects tampering and triggers instant alerts
- 🪪 **RFID Access** – Unlock using registered RFID cards (with bypass logic)
- 📲 **Multi-Platform Remote Control** – Lock/unlock and monitor via mobile, web, and desktop apps
- 🔔 **Live Status Updates** – Real-time updates through Firebase on lock state and package presence

---

## 🧰 Tech Stack

| Layer          | Technologies                                                                 |
|----------------|------------------------------------------------------------------------------|
| **Hardware**   | ESP32, MFRC522 RFID, HX711 Load Cell, Servo Motor, Push Button, LEDs        |
| **Firmware**   | Arduino C++                                                                 |
| **Backend**    | Firebase Realtime Database                                                  |
| **Mobile App** | Kotlin (Android)                                                            |
| **Desktop App**| Python (Kivy)                                                               |
| **Web App**    | HTML, CSS, JavaScript                                                       |

---

## 🏗️ System Architecture

- Package is placed in the box  
- Load Cell detects package weight  
- ESP32 microcontroller processes signals  
  - Sends status to **Firebase Realtime Database**  
  - Triggers **Vibration Sensor** to detect tampering  
  - Uses **RFID Module** for unlock logic  
  - Controls **Servo Motor** to lock/unlock  
- Apps (Mobile / Web / Desktop) fetch real-time updates from Firebase

---

## 📁 Project Structure

-GuardBox/
-├── hardware/
-│ ├── esp32_firmware/
-│ └── circuit_diagram.png
-├── mobile_app/ # Android app (Kotlin)
-├── desktop_app/ # Kivy app (Python)
-├── web_app/ # Web interface (HTML/CSS/JS)
-├── firebase/ # Firebase config & rules
-├── README.md

---

## 📸 Screenshots / Media

<p float="left">
  <img src="https://github.com/user-attachments/assets/cc036a0a-164d-4194-8173-f8cffcefc0a4" width="300"/>
  <img src="https://github.com/user-attachments/assets/76ea97d5-369c-425e-827b-66833e00296b" width="300"/>
  <img src="https://github.com/user-attachments/assets/278e82a4-e7bb-44b5-84f1-4d7482b6db93" width="300"/>
</p>

---

## 👨‍💻 Contributors

- Can OZEL
- Enes ISBILEN
- Zihni AKIN
- Arda SIMSEK
- Furkan AKSOY

---

## 🏫 Academic Context

This project was developed for the **“Special Topics in Computer Engineering (CEN309)”** course at **Maltepe University**, starting in **February 2025**.  
GuardBox is still under active development with continuous feature upgrades and improvements.

---

## 📌 License

This project is licensed under the [MIT License](LICENSE).







