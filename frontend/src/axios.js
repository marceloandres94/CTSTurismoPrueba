import axios from "axios";
import router from "./router"; // Importamos el router para redirigir si es necesario

// Crear una instancia de Axios
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    "Content-Type": "application/json"
  }
});

// Interceptor para agregar el token en las solicitudes
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
// Interceptor para manejar errores de autenticación (como la expiración del token)
api.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      if (error.response.status === 401) {
        // Si recibimos un error 401, redirigir al login
        localStorage.removeItem("token"); // Eliminamos el token si es inválido o ha expirado
        router.push({ name: "Login" });
      }
      return Promise.reject(error);
    }
  );
  

export default api;
