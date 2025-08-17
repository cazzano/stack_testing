# Vue.js Portfolio - Multi-Page Routing Guide

## Introduction

This guide explains how the portfolio has been refactored from a single-page scrolling application to a multi-page application using Vue Router. This change provides a more traditional website experience with distinct URLs for each section and improved navigation.

## Table of Contents

1. [Router Structure](#router-structure)
2. [Navigation](#navigation)
3. [Adding New Pages](#adding-new-pages)
4. [Modifying Existing Pages](#modifying-existing-pages)
5. [Route Guards and Navigation](#route-guards-and-navigation)

## Router Structure

The Vue Router configuration is located in `src/router/index.js`. It defines the following routes:

```javascript
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
```

Each route maps a URL path to a specific component, allowing users to navigate directly to different sections of your portfolio.

## Navigation

The navigation has been updated to use Vue Router's `<router-link>` component instead of scroll-based navigation. This can be found in `src/components/TheHeader.vue`:

```html
<ul class="menu menu-horizontal px-1">
  <li><router-link to="/" class="hover:text-primary">About</router-link></li>
  <li><router-link to="/projects" class="hover:text-primary">Projects</router-link></li>
  <li><router-link to="/skills" class="hover:text-primary">Skills</router-link></li>
  <li><router-link to="/contact" class="hover:text-primary">Contact</router-link></li>
</ul>
```

The `<router-link>` component automatically applies an active class to the current route, making it easy to style the active navigation item.

## Adding New Pages

To add a new page to your portfolio:

1. Create a new Vue component in the `src/views/` directory.
2. Add a new route in `src/router/index.js`:

```javascript
import NewPageView from '../views/NewPageView.vue'

const routes = [
  // existing routes...
  {
    path: '/new-page',
    name: 'newPage',
    component: NewPageView
  }
]
```

3. Add a navigation link in `src/components/TheHeader.vue`:

```html
<li><router-link to="/new-page" class="hover:text-primary">New Page</router-link></li>
```

## Modifying Existing Pages

Each page is now a separate component in the `src/views/` directory. To modify a page, simply edit the corresponding component file:

- About page: `src/views/AboutSection.vue`
- Projects page: `src/views/ProjectsSection.vue`
- Skills page: `src/views/SkillsSection.vue`
- Contact page: `src/views/ContactSection.vue`

## Route Guards and Navigation

Vue Router supports navigation guards that allow you to control navigation behavior. For example, you might want to add a confirmation before leaving a form page:

```javascript
// In your router configuration
{
  path: '/contact',
  name: 'contact',
  component: ContactView,
  beforeLeave: (to, from, next) => {
    if (formHasUnsavedChanges) {
      if (confirm('You have unsaved changes. Are you sure you want to leave?')) {
        next();
      } else {
        next(false);
      }
    } else {
      next();
    }
  }
}
```

## Programmatic Navigation

You can also navigate programmatically using the router instance:

```javascript
import { useRouter } from 'vue-router';

const router = useRouter();

// Navigate to a specific route
router.push('/projects');

// Navigate with named route
router.push({ name: 'projects' });

// Navigate with query parameters
router.push({ path: '/projects', query: { category: 'web' } });
```

This is useful for navigation after form submissions or based on user interactions.

## Conclusion

The multi-page structure provides a more traditional web experience while maintaining the benefits of a single-page application. Users can now bookmark specific pages, use the browser's back/forward buttons naturally, and see meaningful URLs that reflect the current content.

Remember to update your navigation links when adding or removing pages, and consider using route meta fields for additional page-specific information like titles or access control.
