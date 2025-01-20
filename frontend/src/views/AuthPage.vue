<template>
  <div
    class="container-fluid bg-light min-vh-100 d-flex align-items-center justify-content-center py-5"
  >
    <div class="card shadow-sm" style="max-width: 450px">
      <!-- Nav tabs -->
      <div class="card-header bg-white border-bottom-0 pt-4">
        <ul class="nav nav-tabs border-0">
          <li class="nav-item">
            <button
              :class="['nav-link', isLogin ? 'active' : '']"
              @click="isLogin = true"
            >
              Sign In
            </button>
          </li>
          <li class="nav-item">
            <button
              :class="['nav-link', !isLogin ? 'active' : '']"
              @click="isLogin = false"
            >
              Register
            </button>
          </li>
        </ul>
      </div>

      <div class="card-body p-4">
        <!-- Form -->
        <form @submit.prevent="handleSubmit">
          <!-- Registration Fields -->
          <div v-if="!isLogin" class="row g-3 mb-3">
            <div class="col-sm-6">
              <label class="form-label">First Name</label>
              <input
                type="text"
                class="form-control"
                v-model="form.f_name"
                required
              />
            </div>
            <div class="col-sm-6">
              <label class="form-label">Last Name</label>
              <input
                type="text"
                class="form-control"
                v-model="form.l_name"
                required
              />
            </div>
          </div>

          <!-- Common Fields -->
          <div class="mb-3">
            <label class="form-label">Email address</label>
            <input
              type="email"
              class="form-control"
              v-model="form.email"
              required
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <div class="input-group">
              <input
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                v-model="form.password"
                required
              />
              <button
                class="btn btn-outline-secondary"
                type="button"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? "Hide" : "Show" }}
              </button>
            </div>
          </div>

          <!-- Alert for errors -->
          <div v-if="error" class="alert alert-danger py-2" role="alert">
            {{ error }}
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary w-100 mb-3"
            :disabled="loading"
          >
            <span
              v-if="loading"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            {{
              loading
                ? "Please wait..."
                : isLogin
                ? "Sign In"
                : "Create Account"
            }}
          </button>

          <!-- Social Sign In -->
          <div class="text-center mb-3">
            <small class="text-muted">or continue with</small>
          </div>

          <div class="d-flex gap-2 mb-3">
            <button type="button" class="btn btn-light flex-grow-1">
              Google
            </button>
            <button type="button" class="btn btn-light flex-grow-1">
              Facebook
            </button>
          </div>

          <!-- Bottom Text -->
          <div class="text-center">
            <small class="text-muted">
              {{
                isLogin ? "Don't have an account?" : "Already have an account?"
              }}
              <a
                href="#"
                class="text-decoration-none"
                @click.prevent="isLogin = !isLogin"
              >
                {{ isLogin ? "Sign up" : "Sign in" }}
              </a>
            </small>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
const BASE_URL = import.meta.env.VITE_BASE_URL;

export default {
  name: "AuthPage",
  setup() {
    const router = useRouter();
    const isLogin = ref(true);
    const loading = ref(false);
    const error = ref("");
    const showPassword = ref(false);

    const form = reactive({
      f_name: "",
      l_name: "",
      email: "",
      password: "",
    });

    const handleSubmit = async () => {
      try {
        loading.value = true;
        error.value = "";

        const endpoint = isLogin.value
          ? `${BASE_URL}/login`
          : `${BASE_URL}/users`;
        const response = await axios.post(endpoint, form);

        localStorage.setItem("user", JSON.stringify(response.data.user));
        router.push("/");
      } catch (err) {
        error.value =
          err.response?.data?.message || "An error occurred. Please try again.";
      } finally {
        loading.value = false;
      }
    };

    return {
      isLogin,
      form,
      loading,
      error,
      showPassword,
      handleSubmit,
    };
  },
};
</script>

<style scoped>
.bg-light {
  background-color: #f8f9fa !important;
}

.card {
  border: none;
  border-radius: 8px;
}

.nav-tabs .nav-link {
  color: #6c757d;
  border: none;
  padding: 12px 16px;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  border-bottom: 2px solid #0d6efd;
  font-weight: 500;
}

.form-control {
  padding: 0.5rem 0.75rem;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}

.btn-primary {
  padding: 0.5rem;
  font-weight: 500;
}

.btn-light {
  background-color: #f8f9fa;
  border-color: #dee2e6;
}

.btn-light:hover {
  background-color: #e9ecef;
}
</style>
