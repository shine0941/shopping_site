# shopping_site

A full-stack shopping site built with **Django** (backend), **Vue 3** (frontend), **PostgreSQL**, and **Docker**.

## Features

### ✅ Frontend (Vue 3 + Vite + Vuetify)

- User registration and login (with instant login after sign-up)
- Product browsing with filtering and sorting (category, price, time)
- Order placement and status tracking
- Responsive design with Vuetify

### ✅ Backend (Django + DRF)

- JWT-based authentication
- Merchant/admin/customer roles with permission control
- Product/category management
- Orders, order items, coupon logic
- WebSocket live chat (WIP)

### ✅ DevOps

- Dockerized setup with separate containers for:

  - `web` (Django backend)
  - `frontend` (Vue dev server)
  - `db` (PostgreSQL)

- Environment variables loaded via `.env`

---

## Project Structure

```
shopping_site/
├── cart/              # Django backend app
├── chat/              # Django backend app
├── core/              # Django backend app
├── coupons/           # Django backend app
├── orders/            # Django backend app
├── products/          # Django backend app
├── users/             # Django backend app
├── shopping_site/     # Main Django project
├── manage.py
│
├── frontend/          # Vue 3 frontend app (Vite)
│   └── ...
├── docker-compose.yml
└── .env
```

---

## Setup Instructions

### 📦 Requirements

- Docker & Docker Compose
- Node.js + npm (for local frontend dev)

---

### 🐳 Run With Docker

1. **Create `.env`**

```env
# .env
POSTGRES_DB=postgres
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_db_password
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
```

2. **Start services**

```bash
docker compose up --build
```

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend (Vue): [http://localhost:5175](http://localhost:5175) (docker) / [http://localhost:5174](http://localhost:5174) (local)

---

## 🧪 Running Django Commands in Docker

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## 🖥 Local Frontend Dev (Optional)

1. Go to `frontend/`

```bash
cd frontend
npm install
npm run dev
```

> Default port: `5174`

---

## 💠 API Overview

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| POST   | /api/register/ | Register user            |
| POST   | /api/token/    | Get JWT tokens           |
| GET    | /api/products/ | List products            |
| POST   | /api/orders/   | Create order             |
| ...    |                | See `/swagger/` for docs |

---

## 📄 Notes

- Default ordering is `-created_at`
- Sorting via `ordering` query param: `?ordering=-price`
- You can log in as merchant and see only your products

---

## 📷 Sample Image Upload

Images are uploaded to `product_images/` via the `ProductImage` model (related to `Product`).

---

## 🧹 Future Work

- WebSocket live chat
- Order payment integration
- Admin dashboard

---

## License

MIT
