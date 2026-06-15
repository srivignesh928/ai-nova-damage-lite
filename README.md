# AI Powered Vehicle Valuation System with Damage Detection

[![GitHub](https://img.shields.io/badge/GitHub-ai--nova--damage--lite-blue?logo=github)](https://github.com/srivignesh928/ai-nova-damage-lite)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock%20Nova%20Lite-orange?logo=amazon-aws)](https://aws.amazon.com/bedrock/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green?logo=fastapi)](https://fastapi.tiangolo.com/)

## Overview

An AI-powered used vehicle valuation platform that predicts resale value using Machine Learning (XGBoost) and AWS Bedrock Nova Lite for intelligent brand detection and damage analysis.

## ✨ Key Features

### 🚗 Vehicle Price Prediction
- XGBoost ML model for accurate price estimation
- 13 features including brand, model, mileage, age, condition
- Transaction modes: Selling, Buying for Resale, Personal Use
- Dynamic profit margin calculation

### 🔍 AI Brand Detection
- Upload car image → AWS Bedrock detects brand/model
- Auto-fills form with vehicle details
- 90% detection accuracy
- 2-3 second response time

### 🛠️ **NEW: AI Damage Detection**
- Upload damage image → AI generates description
- Detects scratches, dents, broken parts, rust, paint damage
- Severity assessment (none/minor/moderate/major)
- One-click auto-fill with "Use Description" button
- Visual preview with color-coded badges

### 📊 Smart Features
- Prediction history with search
- CSV export functionality
- Printable reports
- Real-time price calculation
- Confidence scoring

## Features

- Vehicle Price Prediction
- FastAPI REST API
- Interactive Swagger Documentation
- Smart Brand/Model Search
- Server-backed Prediction History
- CSV export and printable report
- Health and metadata endpoints
- Professional Frontend
- AI-Based Estimation

## API Endpoints

- `POST /predict` — Get a new valuation
- `GET /brands` — List brands, optional `search` query
- `GET /models/{brand}` — List models for a brand, optional `search` query
- `GET /vehicle/{brand}/{model}` — Get variant and fuel/transmission details
- `GET /history` — Retrieve saved prediction history
- `DELETE /history` — Clear prediction history
- `GET /vehicles` — Search available vehicles
- `GET /metadata` — App metadata and dataset counts
- `GET /health` — Health check

## Tech Stack

- Python
- FastAPI
- XGBoost
- Scikit-learn
- Pandas
- HTML
- CSS
- JavaScript
- GitHub Codespaces

## Current Status

- Data Cleaning ✅
- EDA ✅
- Feature Engineering ✅
- Model Training ✅
- Model Evaluation ✅
- Backend API ✅
- Frontend Integration 🔄