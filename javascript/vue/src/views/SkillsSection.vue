<template>
  <section id="skills" class="py-16 bg-base-100">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-8">My Skills</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Frontend Skills -->
        <div class="card bg-base-200 shadow-xl">
          <div class="card-body">
            <h3 class="card-title text-xl mb-4">
              <font-awesome-icon :icon="['fas', 'code']" class="mr-2 text-primary" />
              Frontend Development
            </h3>
            
            <div class="space-y-4">
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">Vue.js</span>
                  <span>90%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 90%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">JavaScript</span>
                  <span>85%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 85%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">Tailwind CSS</span>
                  <span>95%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 95%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">HTML5 & CSS3</span>
                  <span>90%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 90%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Backend Skills -->
        <div class="card bg-base-200 shadow-xl">
          <div class="card-body">
            <h3 class="card-title text-xl mb-4">
              <font-awesome-icon :icon="['fas', 'server']" class="mr-2 text-primary" />
              Backend Development
            </h3>
            
            <div class="space-y-4">
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">Node.js</span>
                  <span>80%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 80%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">Express.js</span>
                  <span>75%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 75%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">MongoDB</span>
                  <span>70%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 70%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex justify-between mb-1">
                  <span class="font-medium">RESTful APIs</span>
                  <span>85%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-primary h-2.5 rounded-full" style="width: 85%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Tools & Technologies -->
      <div class="mt-8">
        <h3 class="text-xl font-semibold text-center mb-6">Tools & Technologies</h3>
        <div class="flex flex-wrap justify-center gap-4">
          <div class="badge badge-lg p-4">
            <font-awesome-icon :icon="['fab', 'git-alt']" class="mr-2" />
            Git
          </div>
          <div class="badge badge-lg p-4">
            <font-awesome-icon :icon="['fab', 'npm']" class="mr-2" />
            npm/pnpm
          </div>
          <div class="badge badge-lg p-4">
            <font-awesome-icon :icon="['fas', 'terminal']" class="mr-2" />
            Command Line
          </div>
          <div class="badge badge-lg p-4">
            <font-awesome-icon :icon="['fab', 'figma']" class="mr-2" />
            Figma
          </div>
          <div class="badge badge-lg p-4">
            <font-awesome-icon :icon="['fas', 'mobile-alt']" class="mr-2" />
            Responsive Design
          </div>
          <div class="badge badge-lg p-4">
            <font-awesome-icon :icon="['fas', 'code-branch']" class="mr-2" />
            CI/CD
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
