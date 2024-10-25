<template>
  <div class="admin-panel">
    <AppNavbar /> <!-- Agrega la barra de navegación en la parte superior -->
    <div class="panel-container">
      <h2>Panel de Administración</h2>
      <button @click="selectWinner" class="btn">Generar Ganador</button>
      <!-- Usamos v-html para mostrar el contenido con etiquetas HTML -->
      <p v-if="winnerMessage" class="winner-message" v-html="winnerMessage"></p>
      <button @click="logout" class="btn logout-btn">Cerrar Sesión</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AppNavbar from "@/components/Navbar.vue";

export default {
  name: "AdminPanel",
  components: {
    AppNavbar,
  },
  data() {
    return {
      winnerMessage: null,
    };
  },
  methods: {
    async selectWinner() {
      const token = localStorage.getItem("token");
      try {
        const response = await axios.get("http://localhost:8000/api/users/winner/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.winnerMessage = response.data.message;
      } catch (error) {
        console.error(error.response.data);
        alert("Error al generar el ganador: " + error.response.data.message);
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push({ name: "AdminLogin" });
    },
  },
};
</script>

<style scoped>
.admin-panel {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.panel-container {
  max-width: 600px;
  width: 100%;
  text-align: center;
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  font-size: 2rem;
  color: #333;
}

.btn {
  background-color: #333;
  color: white;
  padding: 12px 24px;
  border: none;
  margin: 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #555;
}

.winner-message {
  margin-top: 20px;
  font-size: 1.2rem;
  color: green;
  text-align: center;
}

.logout-btn {
  background-color: #d9534f;
}

.logout-btn:hover {
  background-color: #c9302c;
}
</style>
