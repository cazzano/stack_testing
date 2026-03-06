<template>
  <div class="min-h-screen bg-background font-sans antialiased">
    <Navbar />
    <main class="flex-1">
      <NuxtPage />
    </main>
    <footer class="border-t py-12 md:py-16">
      <div class="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row md:py-0">
        <div class="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
          <LucidePentagon class="h-6 w-6 text-primary" />
          <p class="text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built by <a href="#" class="font-medium underline underline-offset-4">Antigravity</a>. The source code is available on <a href="#" class="font-medium underline underline-offset-4">GitHub</a>.
          </p>
        </div>
        <p class="text-center text-sm text-muted-foreground md:text-left">
          &copy; 2026 Antigravity Inc. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { LucidePentagon } from 'lucide-vue-next'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
}
</style>
