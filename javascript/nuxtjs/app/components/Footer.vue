<template>
  <footer class="border-t bg-background/50 backdrop-blur-xl">
    <div class="container px-4 py-16 md:py-24">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-8">
        <!-- Brand Section -->
        <div class="space-y-6">
          <NuxtLink to="/" class="flex items-center space-x-2">
            <div class="bg-primary rounded-xl p-1 shadow-lg shadow-primary/20">
              <LucidePentagon class="h-6 w-6 text-primary-foreground" />
            </div>
            <span class="inline-block font-bold text-2xl tracking-tight">Antigravity<span class="text-primary">.</span></span>
          </NuxtLink>
          <p class="text-muted-foreground font-medium leading-relaxed max-w-xs">
            Pushing the boundaries of web engineering, one insight at a time. Built with Nuxt 4, Tailwind CSS, and Shadcn-Vue.
          </p>
          <div class="flex items-center gap-4">
            <Button v-for="icon in socialIcons" :key="icon.label" variant="ghost" size="icon" class="rounded-xl bg-muted/50 hover:bg-primary hover:text-primary-foreground transition-all">
              <component :is="icon.icon" class="h-5 w-5" />
            </Button>
          </div>
        </div>

        <!-- Links Sections -->
        <div v-for="section in footerLinks" :key="section.title" class="space-y-6">
          <h3 class="font-black text-sm uppercase tracking-[0.2em] text-foreground/70">{{ section.title }}</h3>
          <ul class="space-y-4">
            <li v-for="link in section.links" :key="link.label">
              <NuxtLink :to="link.to" class="text-muted-foreground font-bold hover:text-primary transition-colors">
                {{ link.label }}
              </NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Newsletter Section -->
        <div class="space-y-6">
          <h3 class="font-black text-sm uppercase tracking-[0.2em] text-foreground/70">The Lab Report</h3>
          <p class="text-sm text-muted-foreground font-medium">Join our weekly newsletter for deep dives into modern web architecture.</p>
          <div class="space-y-3">
            <Input type="email" placeholder="Email address" class="rounded-xl border-primary/10 bg-muted/30 focus-visible:ring-primary/20" />
            <Button class="w-full rounded-xl font-black shadow-lg shadow-primary/20">Subscribe</Button>
          </div>
        </div>
      </div>

      <Separator class="my-12 opacity-50" />

      <div class="flex flex-col md:flex-row justify-between items-center gap-6">
        <p class="text-sm font-bold text-muted-foreground/60">
          © 2026 Antigravity Inc. All rights reserved. Built by the community.
        </p>
        <div class="flex items-center gap-8">
            <NuxtLink to="#" class="text-xs font-black uppercase tracking-widest text-muted-foreground/60 hover:text-primary transition-colors">Privacy</NuxtLink>
            <NuxtLink to="#" class="text-xs font-black uppercase tracking-widest text-muted-foreground/60 hover:text-primary transition-colors">Terms</NuxtLink>
            <NuxtLink to="#" class="text-xs font-black uppercase tracking-widest text-muted-foreground/60 hover:text-primary transition-colors">Cookies</NuxtLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { LucidePentagon, LucideTwitter, LucideGithub, LucideLinkedin, LucideYoutube } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'

const socialIcons = [
    { icon: LucideTwitter, label: 'Twitter' },
    { icon: LucideGithub, label: 'GitHub' },
    { icon: LucideLinkedin, label: 'LinkedIn' },
    { icon: LucideYoutube, label: 'YouTube' },
]

const footerLinks = [
    {
        title: 'Platform',
        links: [
            { label: 'Articles', to: '/articles' },
            { label: 'Components', to: '#' },
            { label: 'Resources', to: '#' },
            { label: 'Guides', to: '#' },
        ]
    },
    {
        title: 'Company',
        links: [
            { label: 'About Us', to: '/about' },
            { label: 'Contact', to: '#' },
            { label: 'Careers', to: '#' },
            { label: 'Enterprise', to: '#' },
        ]
    }
]
</script>
