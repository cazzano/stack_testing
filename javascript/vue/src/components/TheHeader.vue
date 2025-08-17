<template>
  <header class="bg-base-100 shadow-md">
    <div class="navbar container mx-auto px-4">
      <div class="navbar-start">
        <div class="dropdown">
          <label tabindex="0" class="btn btn-ghost lg:hidden">
            <font-awesome-icon :icon="['fas', 'bars']" size="lg" />
          </label>
          <ul tabindex="0" class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
            <li><router-link to="/">About</router-link></li>
            <li><router-link to="/projects">Projects</router-link></li>
            <li><router-link to="/skills">Skills</router-link></li>
            <li><router-link to="/contact">Contact</router-link></li>
          </ul>
        </div>
        <router-link to="/" class="btn btn-ghost normal-case text-xl">My Portfolio</router-link>
      </div>
      <div class="navbar-end hidden lg:flex">
        <ul class="menu menu-horizontal px-1">
          <li><router-link to="/" class="hover:text-primary">About</router-link></li>
          <li><router-link to="/projects" class="hover:text-primary">Projects</router-link></li>
          <li><router-link to="/skills" class="hover:text-primary">Skills</router-link></li>
          <li><router-link to="/contact" class="hover:text-primary">Contact</router-link></li>
        </ul>
        <button @click="toggleTheme" class="btn btn-circle btn-ghost ml-2">
          <font-awesome-icon :icon="['fas', isDarkTheme ? 'sun' : 'moon']" size="lg" />
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';

const isDarkTheme = ref(localStorage.getItem('theme') === 'dark');

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value;
  localStorage.setItem('theme', isDarkTheme.value ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', isDarkTheme.value ? 'dark' : 'light');
};

// Initialize theme on component mount
if (isDarkTheme.value) {
  document.documentElement.setAttribute('data-theme', 'dark');
} else {
  document.documentElement.setAttribute('data-theme', 'light');
}
</script>
