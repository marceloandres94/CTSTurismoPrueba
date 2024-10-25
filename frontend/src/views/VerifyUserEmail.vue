<template>
  <div class="verify-container">
    <h2>Verificando correo electrónico...</h2>
    <p v-if="message">{{ message }}</p>

    <div v-if="showPasswordForm" class="password-form">
      <h3>Establecer Contraseña</h3>
      <form @submit.prevent="setPassword">
        <div class="input-group">
          <label for="password">Nueva Contraseña:</label>
          <input v-model="password" id="password" type="password" required />
        </div>
        <button type="submit" class="btn">Guardar Contraseña</button>
      </form>
      <p v-if="passwordMessage" class="password-message">{{ passwordMessage }}</p>
    </div>
  </div>
</template>

<script>
import api from "@/axios";

export default {
  data() {
    return {
      message: null,
      showPasswordForm: false,
      password: "",
      passwordMessage: null,
    };
  },
  async mounted() {
    const { uid, token } = this.$route.params;
    try {
      const response = await api.get(`/users/verify/${uid}/${token}/`);
      this.message = response.data.message || "Correo verificado correctamente.";
      this.showPasswordForm = true; // Mostrar el formulario de contraseña tras la verificación exitosa
    } catch (error) {
      console.error(error.response?.data);
      this.message = error.response?.data?.error || "Error en la verificación.";
    }
  },
  methods: {
    async setPassword() {
      try {
        const response = await api.put("/users/set-password/", {
          uid: this.$route.params.uid,
          token: this.$route.params.token,
          password: this.password,
        });

        // Usa el contenido de 'response' para mostrar un mensaje específico
        this.passwordMessage = response.data.message || "Contraseña establecida exitosamente. Ahora puedes iniciar sesión.";

        // Redirige al usuario al inicio de sesión después de 2 segundos
        setTimeout(() => {
          this.$router.push({ name: "UserRegister" });
        }, 2000);
      } catch (error) {
        // Captura y muestra los errores específicos de validación de contraseña
        this.passwordMessage = error.response?.data?.password ? error.response.data.password.join(" ") : "Error al establecer la contraseña.";
        console.error(error.response?.data);
      }
    },
  },
};
</script>

<style scoped>
.verify-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background-color: #f5f5f5;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
}

.password-form {
  width: 100%;
  max-width: 400px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

.input-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
  width: 100%;
  text-align: center;
}

.btn:hover {
  background-color: #0056b3;
}

.password-message {
  margin-top: 1rem;
  font-size: 1rem;
  color: green;
  text-align: center;
}
</style>
