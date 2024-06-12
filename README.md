# EY_Multiprocessing

Installation
Step 1: Install Dependencies
Navigate to the project directory and install the required dependencies using pip:
cd django_multiprocessing
pip install -r requirements.txt
Step 2: Apply Database Migrations
Apply database migrations to create the necessary database schema:
python manage.py migrate
Usage
Step 1: Start the Development Server
Start the Django development server:
python manage.py runserver
Step 2: Access the API Endpoint
Navigate to the following URL in your web browser or API client:
http://localhost:8000/api/add/
Step 3: Submit POST Requests
Submit POST requests with JSON payload to the API endpoint. The payload should be in the
following format:
{
&quot;batchid&quot;: &quot;id0101&quot;,
&quot;payload&quot;: [[1, 2], [3, 4]]
}

Testing
To run the unit tests, use the following command:
python manage.py test
