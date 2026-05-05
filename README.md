Tamil Nadu Election Live Tracker 2026

A comprehensive, real-time election tracking dashboard built to monitor and visualize the 2026 Tamil Nadu Assembly Elections. This full-stack application automates data extraction from the official Election Commission of India (ECI) website and renders it on an interactive geographical map of Tamil Nadu.


Acknowledgements & Data Availability

AI Assistance: This entire full-stack project (including the web scraper, backend architecture, and React frontend) was developed with the assistance of Google's Gemini AI.
Open Source Data: The election data scraped and utilized in this repository is completely open-source. Researchers, students, and developers are free to download and use the data for independent analysis and data science projects.


Architecture & Technology Stack
The project is divided into three main components:
1. 🕷️ Automated Web Scraper (Python)
LibraryPurposeSelenium WebDriver (Edge)Bypassing basic firewall and pagination restrictionsBeautifulSoup4Parsing complex HTML table structuresRegular Expressions (Regex)Smart text cleaning and name matching
2. ⚙️ Backend API (Django)
LibraryPurposeDjango & Django REST FrameworkCreating RESTful API endpointsSQLite DatabaseLightweight, efficient real-time data storage
3. 🎨 Frontend Dashboard (React.js)
LibraryPurposeReact.jsUser interface and state managementReact-LeafletRendering the interactive GeoJSON map of Tamil Nadu constituenciesTailwind CSSResponsive and modern UI styling

✨ Key Features

  Real-Time Automated Scraping — The Python scraper autonomously navigates through multiple paginated ECI result pages, extracts live trends, and updates the database without manual intervention.

  Smart Name Resolution Engine — Implements a custom text-cleaning algorithm to map discrepancies between ECI official constituency names and standard GeoJSON properties (handling typos, whitespace, and special characters).

  Interactive Map Visualization — Constituencies dynamically change color based on the leading or winning party. Darker shades indicate declared wins, while lighter shades indicate leads.

  Live Analytics Panel — Calculates and displays the overall state-wise party standings and individual constituency details in a live summary box.


Local Installation and Setup
Prerequisites

Python 3.8+
Node.js & npm
Microsoft Edge Browser (for Selenium WebDriver)


Step 1 — Backend Setup

Navigate to the backend directory and set up the Django environment:
bash# Install required Python packages
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
python manage.py runserver

Step 2 — Start the Scraper

Open a new terminal, ensure your virtual environment is active, and run the scraper to start fetching live data:
bashpython live_scraper.py

Note: Keep this terminal running in the background. It will automatically fetch data at 5-minute intervals.


Step 3 — Frontend Setup

Open a third terminal window, navigate to your React application directory:
bash# Install Node dependencies
npm install

# Start the React development server
npm start
The application will be accessible at http://localhost:3000

📄 License
This project is licensed under the MIT License.
You are free to modify, distribute, and use this project for both personal and commercial purposes.