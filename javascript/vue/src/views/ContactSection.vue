<template>
  <section id="contact" class="py-16 bg-base-200">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-8">Contact Me</h2>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Contact Form -->
        <div class="card bg-base-100 shadow-xl">
          <div class="card-body">
            <h3 class="card-title text-xl mb-4">
              <font-awesome-icon :icon="['fas', 'envelope']" class="mr-2 text-primary" />
              Send Me a Message
            </h3>
            
            <form @submit.prevent="handleSubmit">
              <div class="form-control mb-4">
                <label class="label">
                  <span class="label-text">Name</span>
                </label>
                <input type="text" v-model="form.name" placeholder="Your Name" class="input input-bordered" required />
              </div>
              
              <div class="form-control mb-4">
                <label class="label">
                  <span class="label-text">Email</span>
                </label>
                <input type="email" v-model="form.email" placeholder="your.email@example.com" class="input input-bordered" required />
              </div>
              
              <div class="form-control mb-4">
                <label class="label">
                  <span class="label-text">Subject</span>
                </label>
                <input type="text" v-model="form.subject" placeholder="Subject" class="input input-bordered" required />
              </div>
              
              <div class="form-control mb-6">
                <label class="label">
                  <span class="label-text">Message</span>
                </label>
                <textarea v-model="form.message" class="textarea textarea-bordered h-32" placeholder="Your message here..." required></textarea>
              </div>
              
              <div class="form-control">
                <button type="submit" class="btn btn-primary">
                  <font-awesome-icon :icon="['fas', 'paper-plane']" class="mr-2" />
                  Send Message
                </button>
              </div>
            </form>
          </div>
        </div>
        
        <!-- Contact Information -->
        <div class="flex flex-col gap-6">
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h3 class="card-title text-xl mb-4">
                <font-awesome-icon :icon="['fas', 'map-marker-alt']" class="mr-2 text-primary" />
                Location
              </h3>
              <p>San Francisco, CA, United States</p>
            </div>
          </div>
          
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h3 class="card-title text-xl mb-4">
                <font-awesome-icon :icon="['fas', 'envelope']" class="mr-2 text-primary" />
                Email
              </h3>
              <p><a href="mailto:contact@example.com" class="link link-primary">contact@example.com</a></p>
            </div>
          </div>
          
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h3 class="card-title text-xl mb-4">
                <font-awesome-icon :icon="['fas', 'phone']" class="mr-2 text-primary" />
                Phone
              </h3>
              <p><a href="tel:+11234567890" class="link link-primary">+1 (123) 456-7890</a></p>
            </div>
          </div>
          
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h3 class="card-title text-xl mb-4">
                <font-awesome-icon :icon="['fas', 'share-alt']" class="mr-2 text-primary" />
                Social Media
              </h3>
              <div class="flex gap-4">
                <a href="https://github.com" target="_blank" class="btn btn-circle btn-outline">
                  <font-awesome-icon :icon="['fab', 'github']" />
                </a>
                <a href="https://linkedin.com" target="_blank" class="btn btn-circle btn-outline">
                  <font-awesome-icon :icon="['fab', 'linkedin']" />
                </a>
                <a href="https://twitter.com" target="_blank" class="btn btn-circle btn-outline">
                  <font-awesome-icon :icon="['fab', 'twitter']" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive } from 'vue';

const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
});

const handleSubmit = () => {
  // In a real application, you would send this data to a backend
  console.log('Form submitted:', form);
  alert('Thank you for your message! I will get back to you soon.');
  
  // Reset form
  form.name = '';
  form.email = '';
  form.subject = '';
  form.message = '';
};
</script>
