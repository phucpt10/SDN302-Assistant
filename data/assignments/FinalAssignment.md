# 📑 Final Assignment — SDN302 Server-Side Development with NodeJS, Express, and MongoDB

**Course:** SDN302 — Server-Side development with NodeJS, Express, and MongoDB  
**Contribution:** 20% of course  
**Duration:** ~5 weeks (average student)  
**Learning Outcomes (CLOs):** CLO1 → CLO8  

---

## 🎯 Learning Outcomes
- Develop a fully functional Node.js backend application using Express.js.  
- Implement RESTful APIs with proper routing, middleware, and database integration.  
- Utilize MongoDB & Mongoose for data persistence.  
- Implement user authentication & security.  
- Run the backend application locally OR deploy using Firebase Functions / Express server on cloud (Heroku, Render, Railway).  
- Follow best practices in system architecture, API design, and database modeling.  

---

## ⚠️ Plagiarism Policy
Plagiarism includes:
- Copying from the Web/books without reference.  
- Submitting joint work as individual effort.  
- Copying another student’s work.  
- Buying/stealing coursework.  

➡️ Suspected plagiarism will be investigated → failure of the course.  
➡️ All copied/adapted material must be **referenced correctly**.  

---

## 📝 Assignment Submission Requirements
- **Source code** zipped (.zip).  
- **Document Report** (NodeJS app, Database design, Presentation slides).  
- ⚠️ Thiếu một trong các thành phần → không được phép demo.  

---

## 📌 Assignment Topic
**Develop a Full-Stack E-Commerce API using Node.js & MongoDB.**  
- RESTful API for e-commerce platform: browsing, purchasing, managing products.  

---

## 📂 Project Requirements

### 1. Team Formation
- Group of 3–5 members.  
- Each member responsible for at least **one key feature**.  
- Provide short project intro.  

### 2. Case Study
- Brief description of the system.  
- Identify challenges & solutions for backend development.  

### 3. Business Analysis / System Design
- Identify user roles (Admin, User).  
- Define business rules (e.g., “Orders cannot be canceled after payment”).  
- Provide:  
  - RESTful API design (list endpoints).  
  - Database schema (ERD, MongoDB).  
  - System architecture diagram.  

### 4. Backend Development (50%)
- Use Express Router (modular structure).  
- Implement middleware (error handling, auth, security).  
- Use MongoDB (cloud hosting).  
- Follow REST API principles.  
- Add meaningful code comments.  

### 5. Frontend
- Use React.js frontend.  
- Must interact with backend APIs.  
- Include authentication, product listing, order management.  

### 6. Deployment & Security
- Deploy backend with Firebase Functions OR cloud (Heroku, Render, Railway).  
- Use `.env` for sensitive data.  
- Configure CORS.  
- Ensure validation & error handling.  

### 7. Demo
- Live demo of API.  
- Explain functionality + answer instructor questions.  

### 8. Conclusion & Discussion
- Pros & cons of the app.  
- Lessons learned.  
- Future improvements.  

---

## 🏆 Evaluation Criteria

| Task | Score | Conditions |
|------|-------|------------|
| Case Study | 5% | Clear explanation of requirements |
| Business Analysis & System Design | 15% | Well-structured API + DB design |
| Backend Development | 50% | Fully functional API, modular, DB integrated |
| Deployment & Security | 15% | Cloud deploy, security measures |
| Documentation & Presentation | 15% | Clear report, good demo |

➡️ Each member’s contribution must be evaluated.  

---

## 📌 Implementation Notes
- Upload source code to Edunext (with comments).  
- Demo (15 mins, PPT slides).  
- Each member presents their own feature.  

---

## 📋 Assignment Sample

**Objective:** NodeJS app for Product Sale.  
**Features:**  

| Feature | Description | Assigned |
|---------|-------------|----------|
| Authentication | JWT auth, bcrypt password hashing | Member 1 |
| Product Management | CRUD products | Member 2 |
| Cart & Order Processing | Cart, checkout, order placement | Member 3 |
| Payment Integration (Optional) | Simulate payment (Stripe API) | Member 4 |
| User Profile | Update profile, order history | Member 5 |

**Sample API Endpoints:**  
- **Auth (Member 1):**  
  - `POST /api/auth/signup` — Register user  
  - `POST /api/auth/login` — Login + JWT  

- **Products (Member 2):**  
  - `GET /api/products` — Get all  
  - `POST /api/products` — Create product (Admin)  
  - `PUT /api/products/:id` — Update (Admin)  
  - `DELETE /api/products/:id` — Delete (Admin)  

- **Cart & Orders (Member 3):**  
  - `POST /api/cart` — Add to cart  
  - `GET /api/cart` — View cart  
  - `POST /api/order` — Place order  

- **Payment (Optional, Member 4):**  
  - `POST /api/payment` — Simulate payment  

- **User Profile (Member 5):**  
  - `GET /api/user/profile` — Get profile  
  - `PUT /api/user/profile` — Update profile  

---
