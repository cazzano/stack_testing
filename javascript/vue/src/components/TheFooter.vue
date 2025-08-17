<template>
  <footer class="footer footer-center p-10 bg-base-200 text-base-content mt-10">
    <div>
      <div class="grid grid-flow-col gap-4">
        <a href="https://github.com" target="_blank" class="btn btn-ghost btn-circle">
          <font-awesome-icon :icon="['fab', 'github']" size="lg" />
        </a>
        <a href="https://linkedin.com" target="_blank" class="btn btn-ghost btn-circle">
          <font-awesome-icon :icon="['fab', 'linkedin']" size="lg" />
        </a>
        <a href="https://twitter.com" target="_blank" class="btn btn-ghost btn-circle">
          <font-awesome-icon :icon="['fab', 'twitter']" size="lg" />
        </a>
      </div>
    </div> 
    <div>
      <p>Copyright © {{ new Date().getFullYear() }} - All rights reserved</p>
    </div>
  </footer>
</template>
