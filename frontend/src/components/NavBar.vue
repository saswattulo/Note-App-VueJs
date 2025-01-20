<template>
  <nav class="navbar">
    <!-- Logo/Brand section -->
    <div class="navbar-brand">
      <router-link to="/" class="brand-logo">
        <span class="brand-text">YourBrand</span>
      </router-link>
    </div>

    <!-- Navigation links -->
    <div class="navbar-links">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/" class="nav-link">About</router-link>
      <router-link to="/" class="nav-link">Services</router-link>
      <router-link to="/" class="nav-link">Contact</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
};
</script>

<style>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1a1a1a;
  border-bottom: 1px solid #333;
  width: 100%;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.brand-text {
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #646cff;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    padding: 1rem;
  }

  .navbar-links {
    margin-top: 1rem;
    gap: 1rem;
  }
}

/* Light theme support */
@media (prefers-color-scheme: light) {
  .navbar {
    background-color: #ffffff;
    border-bottom: 1px solid #eaeaea;
  }
}
</style>
