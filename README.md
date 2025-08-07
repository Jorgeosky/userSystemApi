# User System API

Bienvenido a **User System API**, un backend desarrollado con Django y Django REST Framework para la gestión de usuarios, autenticación y administración de roles.

---

## 🚀 Características principales

- **Registro de usuarios** sin autenticación
- **Autenticación JWT** (login y refresh)
- **Gestión de usuarios** (listar, editar, eliminar)
- **Roles y permisos** (admin, usuario)
- **Creación automática de superadmin** (`admin` / `admin`)
- **Endpoints protegidos** según permisos

---

## 🛠️ Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/tuusuario/userSystemApi.git
   cd userSystemApi
   ```

2. **Crea y activa el entorno virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instala dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplica migraciones:**

   ```bash
   python manage.py migrate
   ```

5. **Inicia el servidor:**
   ```bash
   python manage.py runserver
   ```

---

## 🔑 Autenticación

- **Login:**  
  `POST /api/token/`

  ```json
  {
    "username": "admin",
    "password": "admin"
  }
  ```

  Respuesta:

  ```json
  {
    "access": "JWT_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
  ```

- **Refresh:**  
  `POST /api/token/refresh/`

---

## 📚 Endpoints principales

| Método | Endpoint       | Descripción      | Autenticación |
| ------ | -------------- | ---------------- | ------------- |
| POST   | `/users/`      | Crear usuario    | ❌            |
| GET    | `/users/`      | Listar usuarios  | ✅            |
| GET    | `/users/{id}/` | Ver usuario      | ✅            |
| PUT    | `/users/{id}/` | Editar usuario   | ✅            |
| DELETE | `/users/{id}/` | Eliminar usuario | ✅            |

---

## 🧑‍💻 Superadmin por defecto

Al aplicar las migraciones, se crea automáticamente el usuario:

- **Usuario:** `admin`
- **Email:** `admin@localhost`
- **Contraseña:** `admin`

---

## 📦 Estructura del proyecto

```
userSystemApi/
├── users/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── ...
├── manage.py
├── requirements.txt
└── ...
```

---

## 📝 Notas

- Recuerda cambiar la contraseña del superadmin en producción.
- Puedes personalizar los roles y permisos en `models.py` y `views.py`.
- Para integración con frontend, consulta la documentación de la API.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

¡Gracias por usar **User System API**!  
¿Dudas o sugerencias? Abre un issue o contacta al equipo
