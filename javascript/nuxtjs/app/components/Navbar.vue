<template>
  <header class="sticky top-0 z-50 w-full border-b bg-background/80 backdrop-blur-xl supports-[backdrop-filter]:bg-background/60">
    <div class="container flex h-16 items-center justify-between">
      <div class="flex items-center gap-8">
        <NuxtLink to="/" class="flex items-center space-x-2 transition-transform hover:scale-105">
          <div class="bg-primary rounded-xl p-1 shadow-lg shadow-primary/20">
            <LucidePentagon class="h-6 w-6 text-primary-foreground" />
          </div>
          <span class="inline-block font-bold text-xl tracking-tight">Antigravity<span class="text-primary font-black">.</span></span>
        </NuxtLink>

        <!-- Desktop Navigation -->
        <NavigationMenu class="hidden md:flex">
          <NavigationMenuList>
            <NavigationMenuItem>
              <NuxtLink to="/" class="group inline-flex h-9 w-max items-center justify-center rounded-md bg-transparent px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50" active-class="text-primary font-semibold">
                Home
              </NuxtLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NuxtLink to="/articles" class="group inline-flex h-9 w-max items-center justify-center rounded-md bg-transparent px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50" active-class="text-primary font-semibold">
                Articles
              </NuxtLink>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NuxtLink to="/about" class="group inline-flex h-9 w-max items-center justify-center rounded-md bg-transparent px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50" active-class="text-primary font-semibold">
                About
              </NuxtLink>
            </NavigationMenuItem>
          </NavigationMenuList>
        </NavigationMenu>
      </div>

      <div class="flex items-center gap-4">
        <!-- Search -->
        <div class="relative w-full max-w-[240px] hidden lg:block group">
          <LucideSearch class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
          <Input
            v-model="searchQuery"
            type="search"
            placeholder="Search insights..."
            class="pl-9 h-10 bg-muted/40 border-transparent focus:bg-background focus:ring-primary/20 transition-all rounded-xl"
          />
        </div>

        <!-- Desktop Actions -->
        <div class="hidden md:flex items-center gap-2">
            <Button variant="ghost" size="icon" class="rounded-full">
                <LucideBell class="h-5 w-5" />
            </Button>
            <Separator orientation="vertical" class="h-6 mx-2" />
            <Avatar class="h-9 w-9 border-2 border-background shadow-sm">
                <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=Admin" />
                <AvatarFallback>AD</AvatarFallback>
            </Avatar>
        </div>

        <!-- Mobile Menu Toggle -->
        <Sheet>
          <SheetTrigger as-child>
            <Button variant="ghost" size="icon" class="md:hidden rounded-xl">
              <LucideMenu class="h-6 w-6" />
            </Button>
          </SheetTrigger>
          <SheetContent side="right" class="w-[300px] sm:w-[400px] p-0">
             <div class="flex flex-col h-full">
                <div class="p-6 border-b flex items-center gap-3 bg-muted/20">
                    <div class="bg-primary rounded-lg p-1.5">
                        <LucidePentagon class="h-5 w-5 text-primary-foreground" />
                    </div>
                    <span class="font-bold text-lg">Antigravity</span>
                </div>
                <nav class="flex-1 p-4 space-y-2">
                    <NuxtLink v-for="link in navLinks" :key="link.to" :to="link.to" class="flex items-center gap-3 px-4 py-3 rounded-xl text-lg font-medium transition-colors hover:bg-accent active:bg-accent/80" active-class="bg-primary/10 text-primary">
                        <component :is="link.icon" class="h-5 w-5" />
                        {{ link.label }}
                    </NuxtLink>
                </nav>
                <div class="p-6 border-t mt-auto">
                    <Button class="w-full h-12 rounded-xl text-md font-bold shadow-lg shadow-primary/20">Subscribe Now</Button>
                </div>
             </div>
          </SheetContent>
        </Sheet>
      </div>
    </div>
  </header>
</template>

<script setup>
import { LucidePentagon, LucideSearch, LucideMenu, LucideBell, LucideHome, LucideBookOpen, LucideUser } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from '@/components/ui/navigation-menu'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet'
import { Separator } from '@/components/ui/separator'
import { useBlog } from '~/composables/useBlog'

const { searchQuery } = useBlog()

const navLinks = [
    { label: 'Home', to: '/', icon: LucideHome },
    { label: 'Articles', to: '/articles', icon: LucideBookOpen },
    { label: 'About', to: '/about', icon: LucideUser },
]
</script>
