# Random Image + Dominant Color (PySide6)

## Description

A simple GUI application built with PySide6 that:

* Fetches a random image
* Displays it
* Extracts the dominant color from the image

## Features

* GUI using PySide6
* Image processing using Pillow and NumPy
* Dominant color detection
* API integration with API Ninjas

## API Note

The application connects to API Ninjas as required.

However, the `/randomimage` endpoint requires premium access for category-based usage and returns HTTP 400 on the free tier.

To ensure reliability:

* API Ninjas `/quotes` endpoint is used for API connectivity
* A public image service is used to retrieve random images

## How to Run

### Run executable

Open:
dist/main.exe

### Run from source

pip install -r requirements.txt
python main.py

## Technologies Used

* PySide6
* Requests
* Pillow
* NumPy


#Example Output
<img width="599" height="628" alt="image" src="https://github.com/user-attachments/assets/0dcd67ac-97bd-479a-b7f6-dd07fb6a0696" />

