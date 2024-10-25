<template>
    <nav>
      <ul>
        <li><router-link to="/register">Registro</router-link></li>
        <li><router-link to="/login">Admin Login</router-link></li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: "AppNavbar",
  };
  </script>
  
  <style scoped>
  nav {
    background-color: #333;
    padding: 1em;
    position: fixed; /* Hacer que la barra de navegación esté fija en la parte superior */
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }
  
  ul {
    list-style-type: none;
    display: flex;
    justify-content: flex-start; /* Alinear a la izquierda */
    gap: 1em;
    margin: 0;
    padding: 0;
  }
  
  li a {
    color: white;
    text-decoration: none;
    font-weight: bold;
  }
  
  li a:hover {
    text-decoration: underline;
  }
  </style>
  