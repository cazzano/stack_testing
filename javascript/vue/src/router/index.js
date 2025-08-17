import { createRouter, createWebHistory } from 'vue-router'
import AboutView from '../views/AboutSection.vue'
import ProjectsView from '../views/ProjectsSection.vue'
import SkillsView from '../views/SkillsSection.vue'
import ContactView from '../views/ContactSection.vue'

const routes = [
  {
    path: '/',
    name: 'about',
    component: AboutView
  },
  {
    path: '/projects',
    name: 'projects',
    component: ProjectsView
  },
  {
    path: '/skills',
    name: 'skills',
    component: SkillsView
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
