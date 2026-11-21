# Healthcare Management API

A RESTful healthcare backend built using **Django, Django REST Framework, and PostgreSQL**.

## Features

- JWT authentication (registration and login)
- Patient CRUD with user-specific ownership
- Doctor CRUD operations
- Patient-doctor assignment and management
- Input validation and duplicate assignment prevention
- Swagger API documentation
- Automated tests and Postman collection

## Tech Stack

Python 3.13 · Django · Django REST Framework · PostgreSQL · Simple JWT · Docker · drf-spectacular

## Project Structure

```text
healthCare/
├── accounts/
├── patients/
├── doctors/
├── mappings/
├── config/
├── postman/
│   └── HealthCare.postman_collection.json
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── manage.py
└── README.md
```

## Setup Instructions

**1. Clone the repository**

```bash
git clone <your-github-repository-url>
cd healthCare
```

**2. Create virtual environment and install dependencies**

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Configure environment variables**

```bash
cp .env.example .env
```

Update `.env` with your database credentials and Django secret key.

**4. Start PostgreSQL and run migrations**

```bash
docker compose up -d
python manage.py migrate
```

**5. Start the server**

```bash
python manage.py runserver
```

## API Endpoints

| Module | Endpoints |
|---|---|
| Authentication | `POST /api/auth/register/`, `POST /api/auth/login/` |
| Patients | `GET, POST /api/patients/`, `GET, PUT, PATCH, DELETE /api/patients/{id}/` |
| Doctors | `GET, POST /api/doctors/`, `GET, PUT, PATCH, DELETE /api/doctors/{id}/` |
| Mappings | `GET, POST /api/mappings/`, `GET /api/mappings/{patient_id}/`, `DELETE /api/mappings/{id}/` |

Protected endpoints require a JWT access token in the `Authorization: Bearer <access_token>` header.

## API Documentation & Testing

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **OpenAPI Schema:** `http://127.0.0.1:8000/api/schema/`
- **Postman Collection:** `postman/HealthCare.postman_collection.json`

## Run Tests

```bash
python manage.py test
```

## Security

- Environment variables for sensitive configurations.
- JWT authentication for protected endpoints.
- Patient ownership validation.
- Password hashing and duplicate mapping prevention.