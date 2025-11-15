## SweetShop - Full-Stack Web Application
A FastAPI + React Based Sweet Store Management System
SweetShop is a full-stack web application that allows users to browse sweets, purchase items, and manage inventory.
Admin users can add, delete, and restock sweets.
The frontend is pastel-themed, and fully responsive UI. 
This project is a full-stack Sweet Shop management system with:
- A FastAPI backend for authentication, sweet inventory and purchase logic.
- A React frontend (SPA) styled in a pastel sweet-theme design.
- Admin & User dashboards with role-based features.
## Features
- User Registration & Login
- JWT Authentication
- Admin Dashboard (Add / Delete / Restock sweets)
- User Dashboard (Search & Purchase sweets)
- Fully responsive UI matching Canva design
- SQLite database persistence
## Technologies Used
- **Frontend:** React.js, Axios
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Database:** SQLite
- **Auth:** JWT
- **Styling:** Custom CSS + Imported fonts
## Backend Setup
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Run FastAPI backend:
```
uvicorn main:app --reload
```
## Frontend Setup
1. Navigate to `sweet-shop/`
2. Install dependencies:
```
npm install
```
3. Start development server:
```
npm start
```
## API Endpoints
### Auth
- POST `/register`
- POST `/login`
### Sweets
- GET `/sweets`
- POST `/sweets`
- DELETE `/sweets/{id}`
- POST `/sweets/{id}/purchase`
- POST `/sweets/{id}/restock`
## Project Structure
- Backend: root folder (`main.py`, `models.py`, etc.)
- Frontend: `/sweet-shop` containing React pages:
- Welcome
- Register
- Login
- UserDashboard
- AdminDashboard
## Git Usage
<img width="870" height="309" alt="Screenshot 2025-11-16 014851" src="https://github.com/user-attachments/assets/8e90e006-092c-4867-b410-fea3202dcb0f" />
<img width="1919" height="1199" alt="Screenshot 2025-11-16 011219" src="https://github.com/user-attachments/assets/93142456-a622-47a6-9c7f-4bb0512eb897" />
<img width="1919" height="1199" alt="Screenshot 2025-11-16 011235" src="https://github.com/user-attachments/assets/233721e9-a2e6-46b5-b073-d1f040e2f000" />

## ScreenShots

- Welcome Page
  <img width="1917" height="1038" alt="Screenshot 2025-11-15 235550" src="https://github.com/user-attachments/assets/55afd2fe-cd93-4e92-9e84-7c7bd2553e89" />
- Registration Page
  <img width="1919" height="1097" alt="Screenshot 2025-11-15 235609" src="https://github.com/user-attachments/assets/275c7dae-f8a8-4866-9d1d-6d24f6d836c6" />
- Login Page
  <img width="1919" height="1098" alt="Screenshot 2025-11-15 235618" src="https://github.com/user-attachments/assets/bf5d9e0b-ef6c-45f4-be2c-dab905da451f" />
- User Dashboard
  <img width="1901" height="1036" alt="Screenshot 2025-11-15 235703" src="https://github.com/user-attachments/assets/cde1e5d6-8eb6-4a29-b7a8-373cfb8fc353" />
- Admin Dashboard
  <img width="1898" height="1036" alt="Screenshot 2025-11-15 235724" src="https://github.com/user-attachments/assets/4c711e5a-bb45-48fb-a039-f7b8d0dc1e9c" />

## Pytest
Run backend tests:
```
pytest
```
<img width="1478" height="659" alt="Screenshot 2025-11-16 005347" src="https://github.com/user-attachments/assets/933c61cc-f0ae-47e9-b342-5bef675f4093" />

## AI Usage Note
ChatGPT was used for:
-Debugging issues such as JWT token errors, CORS problems, and SQLite conflicts - Multi-layer backend debugging
-Understanding how to structure FastAPI routes, models, and authentication - Backend architecture
-Generating and correcting PyTest test cases
