# Lowry Smiplified

Lowry Simplified is a web application designed to help life scientists efficiently manage, analyze, and visualize experiment data. The app focuses on streamlining workflows for experiments that involve photometry, particularly those measuring light absorption in biological samples.

## Problem overview:
Life science experiments often generate large volumes of data, especially when using techniques like photometry, where the absorption of light by a sample is measured. Researchers face several challenges:

- Data Management: Experiment results are often scattered across spreadsheets, notebooks, and instruments, making it difficult to organize and track data.
- Error-Prone Analysis: Manual calculations and plotting can lead to mistakes and inconsistencies.
- Time-Consuming Workflow: Cleaning, normalizing, and analyzing data manually consumes valuable time, delaying insights and conclusions.

Lowry Simplified addresses these issues by providing a centralized, user-friendly platform for data storage, processing, and visualization.


## Features

1. Data Upload & Storage: Easily upload experiment data in common format (CSV) and store it securely in one place.
2. Photometry Analysis: Automatically process and normalize photometry data, including absorbance calculations and background subtraction.
3. Visualization Tools: Generate interactive graphs and charts to visualize trends and results.
4. Export & Reporting: Export processed data and results in multiple formats for further analysis or publication.
5. User-Friendly Interface: Designed for scientists without extensive computational experience.

## Setup
1. clone the repository;
2. Copy `.env-copy` file into `.env` and fill all the variables.  
    *Note:* ALGORITHM - hashing algorithm e.g. HS256;  
            MINIO_ENDPOINT - `http://http://lowry-minio:9000`.
3. Run command - `docker-compose up -d --build`
4. Run command - `docker-compose exec -t backend alembic upgrade head`
5. Open http://localhost:80 - for UI
    / http://localhost:8000/docs - for API

## Usage
#### 1. Register on app
#### 2. Navigate to "standards" and try to create one. keep in mind csv file should have certain format:  
1) X column header must contain: Either "X" or "C" AND Unit inside parenthesis (e.g., **X (mg/ml)**)  
2) Y colums headers must contain either "Y" or "E".
#### 3. Navigate to "projects" and create one;


## Features to be implemented:

### projects:
- [x] Projects CRUD 
- [x] Test Project model and routes
- [x] Frontend

### Experiments:
- [x] CRUD / api
- [x] DE algorithm
- [x] Tests
- [x] Frontend

### Users:
- [x] Sugnup page
- [ ] Password Reset
- [ ] User Update
- [ ] User Profie Page
