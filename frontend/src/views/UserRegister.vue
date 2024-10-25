<template>
  <div class="register-container">
    <AppNavbar /> <!-- Añadir el Navbar aquí -->
    <div class="form-container">
      <h2>Registro de Usuario</h2>
      <form @submit.prevent="registerUser">
        <div class="input-group">
          <label>Email:</label>
          <input v-model="formData.email" type="email" required />
        </div>
        <div class="input-group">
          <label>Nombre:</label>
          <input v-model="formData.first_name" type="text" required />
        </div>
        <div class="input-group">
          <label>Apellido:</label>
          <input v-model="formData.last_name" type="text" required />
        </div>
        <button type="submit" class="btn">Registrarse</button>
      </form>
      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import AppNavbar from "@/components/Navbar.vue";
import api from "@/axios";

export default {
  name: "UserRegister",
  components: {
    AppNavbar,
  },
  data() {
    return {
      formData: {
        email: "",
        first_name: "",
        last_name: "",
      },
      message: null, // Variable para almacenar el mensaje de respuesta
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await api.post("/users/register/", this.formData);
        this.message = response.data.message || "Registro exitoso. Revisa tu correo para verificar tu cuenta.";
      } catch (error) {
        console.error(error.response);
        this.message = error.response?.data?.detail || error.response?.data?.error || "Error en el registro.";
      }
    },
  },
};
</script>

<style scoped>
/* Contenedor general para centrar el contenido */
.register-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* Mantener el contenido centrado verticalmente */
  padding: 20px;
  background-color: #f5f5f5; /* Fondo gris claro */
}

/* Estilos del formulario */
.form-container {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Sombra sutil */
  width: 100%;
  max-width: 500px;
  text-align: center;
}

/* Agrupaciones de los inputs */
.input-group {
  margin-bottom: 1.5em;
  text-align: left;
}

/* Estilos de las etiquetas */
.input-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5em;
  color: #333;
}

/* Estilos de los inputs */
.input-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Estilo del botón */
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
  background-color: #0056b3; /* Cambia el color al pasar el mouse */
}

/* Mensaje de confirmación */
.message {
  color: green;
  margin-top: 1.5em;
  font-weight: bold;
}
</style>
