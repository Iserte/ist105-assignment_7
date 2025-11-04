# 🚗 OpenRouteService Directions Parser

A Python application that retrieves and parses driving directions using the OpenRouteService API. This project was developed for **IST105 - Introduction to Programming**, Assignment #7.

## 📌 Overview

This script allows users to input a starting location and destination, then fetches route data including duration, distance, and step-by-step instructions. It uses the OpenRouteService Directions and Geocoding APIs to process and display travel information.

## 🔧 Features

- Geocodes user-provided addresses
- Retrieves driving directions via POST request
- Parses JSON response for:
  - Trip duration (in minutes)
  - Distance (in kilometers)
  - Step-by-step instructions
- Handles invalid input and API errors
- Includes a quit option for graceful exit
