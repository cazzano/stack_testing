<template>
  <section id="about" class="py-16 bg-base-100">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-8">About Me</h2>
      <div class="flex flex-col lg:flex-row items-center gap-8">
        <div class="lg:w-1/3">
          <div class="avatar">
            <div class="w-64 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2 mx-auto">
              <img src="https://placehold.co/400x400/png" alt="Profile" />
            </div>
          </div>
        </div>
        <div class="lg:w-2/3">
          <div class="card bg-base-200 shadow-xl">
            <div class="card-body">
              <h3 class="card-title text-2xl mb-4">Hello, I'm <span class="text-primary">Your Name</span></h3>
              <p class="mb-4">
                I am a passionate web developer with expertise in modern frontend technologies. 
                I specialize in creating responsive, user-friendly web applications using Vue.js, 
                Tailwind CSS, and other cutting-edge tools.
              </p>
              <p class="mb-4">
                With a strong foundation in web development principles and a keen eye for design, 
                I strive to build applications that are not only functional but also aesthetically pleasing.
              </p>
              <div class="flex flex-wrap gap-2 mt-4">
                <div class="badge badge-primary">Vue.js</div>
                <div class="badge badge-primary">Tailwind CSS</div>
                <div class="badge badge-primary">JavaScript</div>
                <div class="badge badge-primary">HTML5</div>
                <div class="badge badge-primary">CSS3</div>
                <div class="badge badge-primary">Responsive Design</div>
              </div>
              <div class="card-actions justify-end mt-6">
                <a href="#contact" class="btn btn-primary">
                  <font-awesome-icon :icon="['fas', 'envelope']" class="mr-2" />
                  Contact Me
                </a>
                <a href="#" class="btn btn-outline">
                  <font-awesome-icon :icon="['fas', 'file']" class="mr-2" />
                  Download CV
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
