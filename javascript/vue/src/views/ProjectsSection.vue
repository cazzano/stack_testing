<template>
  <section id="projects" class="py-16 bg-base-200">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-8">My Projects</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Project Card 1 -->
        <div class="card bg-base-100 shadow-xl">
          <figure><img src="https://placehold.co/600x400/png" alt="Project 1" /></figure>
          <div class="card-body">
            <h3 class="card-title">
              E-commerce Website
              <div class="badge badge-secondary">Vue</div>
            </h3>
            <p>A fully responsive e-commerce platform with product filtering, cart functionality, and payment integration.</p>
            <div class="flex flex-wrap gap-2 mt-2">
              <div class="badge badge-outline">Vue.js</div>
              <div class="badge badge-outline">Tailwind CSS</div>
              <div class="badge badge-outline">Pinia</div>
            </div>
            <div class="card-actions justify-end mt-4">
              <a href="#" class="btn btn-sm btn-primary">
                <font-awesome-icon :icon="['fas', 'eye']" class="mr-1" />
                Live Demo
              </a>
              <a href="#" class="btn btn-sm btn-outline">
                <font-awesome-icon :icon="['fab', 'github']" class="mr-1" />
                Code
              </a>
            </div>
          </div>
        </div>

        <!-- Project Card 2 -->
        <div class="card bg-base-100 shadow-xl">
          <figure><img src="https://placehold.co/600x400/png" alt="Project 2" /></figure>
          <div class="card-body">
            <h3 class="card-title">
              Task Management App
              <div class="badge badge-secondary">SPA</div>
            </h3>
            <p>A task management application with drag-and-drop functionality, task categorization, and progress tracking.</p>
            <div class="flex flex-wrap gap-2 mt-2">
              <div class="badge badge-outline">Vue.js</div>
              <div class="badge badge-outline">DaisyUI</div>
              <div class="badge badge-outline">Firebase</div>
            </div>
            <div class="card-actions justify-end mt-4">
              <a href="#" class="btn btn-sm btn-primary">
                <font-awesome-icon :icon="['fas', 'eye']" class="mr-1" />
                Live Demo
              </a>
              <a href="#" class="btn btn-sm btn-outline">
                <font-awesome-icon :icon="['fab', 'github']" class="mr-1" />
                Code
              </a>
            </div>
          </div>
        </div>

        <!-- Project Card 3 -->
        <div class="card bg-base-100 shadow-xl">
          <figure><img src="https://placehold.co/600x400/png" alt="Project 3" /></figure>
          <div class="card-body">
            <h3 class="card-title">
              Weather Dashboard
              <div class="badge badge-secondary">API</div>
            </h3>
            <p>A weather dashboard that displays current and forecasted weather data with interactive charts and location search.</p>
            <div class="flex flex-wrap gap-2 mt-2">
              <div class="badge badge-outline">Vue.js</div>
              <div class="badge badge-outline">Tailwind CSS</div>
              <div class="badge badge-outline">Chart.js</div>
            </div>
            <div class="card-actions justify-end mt-4">
              <a href="#" class="btn btn-sm btn-primary">
                <font-awesome-icon :icon="['fas', 'eye']" class="mr-1" />
                Live Demo
              </a>
              <a href="#" class="btn btn-sm btn-outline">
                <font-awesome-icon :icon="['fab', 'github']" class="mr-1" />
                Code
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
