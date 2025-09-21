# 📘 SDN302 — Server-Side Development with NodeJS, Express, and MongoDB

## Giới thiệu môn học
Môn học cung cấp kiến thức và kỹ năng phát triển ứng dụng **web server-side** dựa trên NodeJS, ExpressJS, NestJS, Hono và MongoDB.  
Sinh viên sẽ được thực hành CRUD, xây dựng REST API, tích hợp bảo mật và triển khai ứng dụng.

## Mục tiêu
- Hiểu nguyên lý hoạt động của NodeJS, Express, NestJS, Hono.  
- Thao tác với MongoDB bằng Mongoose.  
- Xây dựng REST API hoàn chỉnh.  
- Hiểu & áp dụng cơ chế Authentication, HTTPS, CORS, OAuth.  
- Tích hợp Frontend (React) với Backend.  
- Deploy ứng dụng server-side trên môi trường thực tế (Heroku, Hosting services).  

## CLOs (Course Learning Outcomes)
- **CLO1:** Hiểu Node, Node modules, API, Node HTTP server.  
- **CLO2:** Sử dụng Express/NestJS/Hono để xây dựng REST API.  
- **CLO3:** Tạo ứng dụng Express bằng Express Generator.  
- **CLO4:** Sử dụng MongoDB & Mongoose để quản lý dữ liệu.  
- **CLO5:** Xây dựng REST API với Express, MongoDB, Mongoose.  
- **CLO6:** Cài đặt Authentication & Security cho ứng dụng.  
- **CLO7:** Sử dụng Backend-as-a-Service (BaaS).  
- **CLO8:** Sử dụng EJS và Handlebars cho templating.  

## Cài đặt môi trường (Environment Setup)
1. **Cài Node.js & npm**  
   - Tải từ [Node.js official](https://nodejs.org/) (chọn LTS version).  
   - Kiểm tra:  
     ```bash
     node -v
     npm -v
     ```  
2. **IDE/Editor khuyến nghị**: [Visual Studio Code](https://code.visualstudio.com/)  
3. **Cài MongoDB**  
   - Local: [MongoDB Community Edition](https://www.mongodb.com/try/download/community)  
   - Hoặc dùng dịch vụ cloud: [MongoDB Atlas](https://www.mongodb.com/atlas)  
4. **Công cụ hỗ trợ**  
   - Postman (test API)  
   - MongoDB Compass (GUI cho MongoDB)  
   - Git (quản lý source code)  
5. **Khởi tạo project**  
   ```bash
   mkdir sdn302-app && cd sdn302-app
   npm init -y
   npm install express mongoose dotenv
