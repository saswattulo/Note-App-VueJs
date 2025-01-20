<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div class="input-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="Enter your email"
          required
        />
      </div>
      <div class="input-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="Enter your password"
          required
        />
      </div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
      <button type="submit" class="login-btn" :disabled="isLoading">
        {{ isLoading ? "Logging in..." : "Login" }}
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
const BASE_URL = import.meta.env.VITE_BASE_URL;
export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      isLoading: false,
      successMessage: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      this.isLoading = true;
      this.successMessage = "";
      this.errorMessage = "";

      try {
        // Sending POST request to backend API
        const response = await axios.post(`${BASE_URL}/login`, {
          email: this.email,
          password: this.password,
        });

        // Handle success
        this.successMessage = response.data.message;
        console.log(response.data); // Optionally log the user data

        // Optionally, store the user details or token if needed
        // localStorage.setItem("user", JSON.stringify(response.data.user));
      } catch (error) {
        // Handle error
        if (error.response) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "An error occurred. Please try again later.";
        }
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Basic styling for the login form */
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  font-size: 14px;
  margin-bottom: 5px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button.login-btn:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

button.login-btn:hover {
  background-color: #2980b9;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.success-message {
  color: green;
  text-align: center;
  margin-top: 10px;
}
</style>
