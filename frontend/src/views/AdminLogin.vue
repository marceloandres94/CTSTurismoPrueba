<template>
  <div class="admin-login">
    <AppNavbar /> <!-- Agrega la barra de navegación en la parte superior -->
    <div class="login-container">
      <h2>Inicio de Sesión de Administrador</h2>
      <form @submit.prevent="login" class="login-form">
        <div class="input-group">
          <label>Email:</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="input-group">
          <label>Contraseña:</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn">Iniciar Sesión</button>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AppNavbar from "@/components/Navbar.vue"; // Importa AppNavbar

export default {
  components: {
    AppNavbar,
  },
  data() {
    return {
      email: '',
      password: '',
      errorMessage: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/api/token/', {
          email: this.email,
          password: this.password,
        });
        
        const { access, is_superuser, is_staff } = response.data;

        if (is_superuser && is_staff) {
          localStorage.setItem('token', access);
          localStorage.setItem('is_superuser', is_superuser);
          localStorage.setItem('is_staff', is_staff);

          this.$router.push({ name: 'AdminPanel' });
        } else {
          this.errorMessage = 'No tienes permisos para acceder al panel de administración.';
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Error en el inicio de sesión. Verifica tus credenciales.';
      }
    },
  },
};
</script>

<style scoped>
/* Ajustar el contenedor principal para centrar el contenido */
.admin-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh; /* Altura mínima de la vista */
  padding-top: 20px; /* Ajustar espacio para la barra de navegación */
  background-color: #f5f5f5; /* Fondo de la página */
}

/* Contenedor del formulario */
.login-container {
  max-width: 400px;
  width: 100%;
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-top: 10px;
}

/* Estilo de los grupos de entrada */
.input-group {
  margin-bottom: 1.5em;
  text-align: left;
}

.input-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5em;
  color: #333;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Botón de envío */
.btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}

/* Mensaje de error */
.error-message {
  color: red;
  margin-top: 1em;
  font-weight: bold;
  text-align: center;
}
</style>
