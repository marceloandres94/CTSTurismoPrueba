import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Asegúrate de importar el router correctamente

// Crear la aplicación y usar el router

const app = createApp(App);

app.use(router); // Registrar el router con Vue
app.mount('#app'); // Montar la aplicación en el elemento con ID 'app'