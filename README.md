

# API de la Aplicacion MicLing `0.0.1`



## Endpoints

### 1. Registro de Usuario

**POST** `/api/auth/register`

Endpoint para registrar un nuevo usuario.

#### Request Body (JSON)
```json
{
  "username": "string",
  "last_name": "string",
  "password": "string",
  "phone_number": "string",
  "age": 0,
  "gender": "Masculino",
  "institucion": "string",
  "grade": "string",
  "country_origin": "string",
  "language_skills": [
    {
      "language": "English",
      "reading": "A1",
      "writing": "A1",
      "listening": "A1",
      "speaking": "A1"
    }
  ],
  "courses": [
    "English"
  ],
  "email": "string",
  "photo": "string"
}
```

#### Responses:
- **200 OK**: Usuario registrado exitosamente.
  ```json
  "string"
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

### 2. Login de Usuario

**POST** `/api/auth/login`

Endpoint para autenticar un usuario y generar un token de acceso.

#### Request Body (JSON)
```json
{
  "username": "string",
  "password": "string"
}
```

#### Responses:
- **200 OK**: Login exitoso.
  ```json
  "string"
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

### 3. Refrescar el Token de Acceso

**POST** `/api/auth/refresh-token`

Endpoint para refrescar el token de acceso.

#### Parameters:
- **refresh_token** (query parameter): El token de refresco.

#### Responses:
- **200 OK**: Token refrescado exitosamente.
  ```json
  "string"
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

### 4. Obtener Exámenes del Usuario

**GET** `/examenes/`

Obtiene los exámenes de un usuario específico según el token de acceso.

#### Responses:
- **200 OK**: Exámenes obtenidos exitosamente.
  ```json
  [
    {
      "exam_type": "string",
      "res_1": 0,
      "res_2": 0,
      "res_3": 0,
      "res_4": 0,
      "res_5": 0,
      "res_6": 0,
      "res_7": 0,
      "res_8": 0,
      "res_9": 0,
      "res_10": 0,
      "total_percentage": 0,
      "id_examen": 0,
      "user_uid": 0,
      "user_name": "string",
      "creation_date": "2025-01-23T23:32:57.540Z"
    }
  ]
  ```

---

### 5. Crear Examen

**POST** `/examenes/`

Endpoint para crear un nuevo examen.

#### Request Body (JSON)
```json
{
  "exam_type": "string",
  "res_1": 0,
  "res_2": 0,
  "res_3": 0,
  "res_4": 0,
  "res_5": 0,
  "res_6": 0,
  "res_7": 0,
  "res_8": 0,
  "res_9": 0,
  "res_10": 0,
  "total_percentage": 0
}
```

#### Responses:
- **200 OK**: Examen creado exitosamente.
  ```json
  {
    "exam_type": "string",
    "res_1": 0,
    "res_2": 0,
    "res_3": 0,
    "res_4": 0,
    "res_5": 0,
    "res_6": 0,
    "res_7": 0,
    "res_8": 0,
    "res_9": 0,
    "res_10": 0,
    "total_percentage": 0,
    "id_examen": 0,
    "user_uid": 0,
    "user_name": "string",
    "creation_date": "2025-01-23T23:32:57.541Z"
  }
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

### 6. Obtener Todos los Exámenes

**GET** `/examenes/todos/`

Obtiene todos los exámenes sin necesidad de un token.

#### Responses:
- **200 OK**: Exámenes obtenidos exitosamente.
  ```json
  [
    {
      "exam_type": "string",
      "res_1": 0,
      "res_2": 0,
      "res_3": 0,
      "res_4": 0,
      "res_5": 0,
      "res_6": 0,
      "res_7": 0,
      "res_8": 0,
      "res_9": 0,
      "res_10": 0,
      "total_percentage": 0,
      "id_examen": 0,
      "user_uid": 0,
      "user_name": "string",
      "creation_date": "2025-01-23T23:32:57.543Z"
    }
  ]
  ```

---

### 7. Comparar Audios

**POST** `/audios/audios/comparar`

Endpoint para comparar dos audios.

#### Request Body (Multipart Form Data)
- **audio1**: Primer archivo de audio.
- **audio2**: Segundo archivo de audio.

#### Responses:
- **200 OK**: Comparación realizada con éxito.
  ```json
  "string"
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

### 8. Obtener Contenido por Idioma

**GET** `/courses/contenido`

Obtiene el contenido de un idioma específico con un solo módulo, niveles, lecciones y ejercicios.

#### Parameters:
- **language** (query): Idioma específico.

#### Responses:
- **200 OK**: Contenido obtenido exitosamente.
  ```json
  {}
  ```

---

### 9. Obtener Datos del Usuario Autenticado

**POST** `/me`

Obtiene los datos del usuario autenticado según el token de acceso.

#### Request Body (JSON)
```json
{
  "access_token": "string"
}
```

#### Responses:
- **200 OK**: Datos del usuario obtenidos exitosamente.
  ```json
  {
    "user_uid": 0,
    "username": "string",
    "last_name": "string",
    "phone_number": "string",
    "rol": "admin",
    "gender": "string",
    "institucion": "string",
    "grade": "string",
    "creation_date": "2025-01-23T23:32:57.548Z",
    "last_modified": "2025-01-23T23:32:57.548Z",
    "country_origin": "string",
    "courses": ["string"],
    "language_skills": {},
    "age": 0,
    "email": "string",
    "photo": "string"
  }
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

### 10. Actualizar Cursos del Usuario

**PATCH** `/me/courses`

Actualiza los cursos del usuario autenticado.

#### Request Body (JSON)
```json
"string"
```

#### Responses:
- **200 OK**: Cursos actualizados exitosamente.
  ```json
  {
    "user_uid": 0,
    "username": "string",
    "last_name": "string",
    "phone_number": "string",
    "rol": "admin",
    "gender": "string",
    "institucion": "string",
    "grade": "string",
    "creation_date": "2025-01-23T23:32:57.551Z",
    "last_modified": "2025-01-23T23:32:57.551Z",
    "country_origin": "string",
    "courses": ["string"],
    "language_skills": {},
    "age": 0,
    "email": "string",
    "photo": "string"
  }
  ```
- **422 Unprocessable Entity**: Error de validación.
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

---

## Autenticación y Seguridad

La API utiliza tokens JWT para autenticar a los usuarios. Los tokens se deben enviar en las cabeceras de las solicitudes para acceder a los endpoints protegidos.

---

## Requisitos

- Python 3.12.6
- FastAPI
- PostgreSQL
- JWT Authentication

---

## Instalación

1. Clona el repositorio.
2. Crea un entorno virtual e instálalo con `pip install -r requirements.txt`.
3. Configura las variables de entorno para la base de datos y JWT.
4. Ejecuta el servidor con `uvicorn app.main:app --reload`.

--- 

## Licencia

Este proyecto está bajo la Licencia MIT.
```
