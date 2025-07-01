# Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/TaskManagementAPI.git  
cd TaskManagementAPI  

3. Install Dependencies  
pip install fastapi uvicorn sqlalchemy pydantic pytest  

5. Run the Application  
uvicorn main:app --reload  

# API Documentation  
## Swagger UI  
Open in browser: http://127.0.0.1:8000/docs  

# Example API Calls  
Create Task  

curl -X POST http://127.0.0.1:8000/tasks/ \  
  -H "Content-Type: application/json" \  
  -d '{  
        "title": "Math",  
        "description": "Do math homework",  
        "status": "pending",  
        "priority": "high",  
        "assigned_to": "Omar"  
      }'  
