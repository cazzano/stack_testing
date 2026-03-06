<template>
  <div class="relative overflow-hidden pb-24">
    <!-- Decorative Background Gradients -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[600px] -z-10 bg-[radial-gradient(circle_at_top,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent opacity-60"></div>
    <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-500/10 rounded-full blur-[120px] -z-20"></div>
    <div class="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-purple-500/10 rounded-full blur-[100px] -z-20"></div>

    <!-- Hero Section -->
    <section class="container px-4 pt-20 pb-32 flex flex-col items-center text-center">
      <div class="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm font-medium text-primary mb-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
        <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
        </span>
        Crafting the Web of Tomorrow
      </div>
      <h1 class="text-5xl md:text-7xl font-black tracking-tight mb-8 leading-[1.05] max-w-4xl text-balance animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-150">
        The Future of <br />
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-600">Digital Experience</span> is Here
      </h1>
      <p class="text-xl md:text-2xl text-muted-foreground/80 mb-12 max-w-2xl text-balance animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-300 font-medium">
        Insightful explorations into Nuxt 4, advanced CSS, and the art of engineering beautiful user interfaces.
      </p>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-16 duration-1000 delay-500">
        <NuxtLink to="/articles">
          <Button size="lg" class="h-14 px-10 text-lg font-bold rounded-2xl shadow-2xl shadow-primary/30 transition-all hover:scale-105 active:scale-95">
            Read Articles
          </Button>
        </NuxtLink>
        <Button size="lg" variant="outline" class="h-14 px-10 text-lg font-bold rounded-2xl bg-background/50 backdrop-blur-sm border-primary/20 hover:bg-background/80 transition-all">
          Our Vision
        </Button>
      </div>
    </section>

    <!-- Recent Posts Section -->
    <section class="container px-4 mt-12">
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <div class="space-y-2">
          <h2 class="text-3xl md:text-4xl font-black tracking-tight">Curated Insights</h2>
          <p class="text-lg text-muted-foreground font-medium">The latest thoughts from our engineering team</p>
        </div>
        <NuxtLink to="/articles">
          <Button variant="link" class="text-lg font-bold text-primary p-0 h-auto group">
            Explore Collection 
            <LucideArrowRight class="ml-2 h-5 w-5 transition-transform group-hover:translate-x-1" />
          </Button>
        </NuxtLink>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <Card v-for="(post, index) in posts.slice(0, 3)" :key="post.id" 
              class="group relative flex flex-col h-full border-none bg-background/50 backdrop-blur-sm shadow-[0_0_50px_-12px_rgba(0,0,0,0.12)] hover:shadow-[0_0_50px_-6px_rgba(0,0,0,0.18)] transition-all duration-500 rounded-[2.5rem] overflow-hidden animate-in fade-in slide-in-from-bottom-12 duration-1000"
              :style="{ transitionDelay: `${index * 150}ms` }">
          
          <div class="aspect-[16/10] relative overflow-hidden m-4 rounded-[1.75rem]">
            <img :src="post.image" :alt="post.title" class="object-cover w-full h-full transform transition-transform duration-700 group-hover:scale-110" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="absolute top-4 left-4">
              <Badge class="bg-white/20 backdrop-blur-md text-white border-white/20 px-3 py-1 font-bold rounded-lg">{{ post.category }}</Badge>
            </div>
          </div>

          <CardHeader class="px-8 pt-2">
            <div class="flex items-center gap-3 text-sm font-bold text-muted-foreground/60 tracking-wider uppercase mb-3">
              <span>{{ post.date }}</span>
              <span class="w-1 h-1 rounded-full bg-primary/40"></span>
              <span>{{ post.readTime }}</span>
            </div>
            <CardTitle class="text-2xl font-black leading-snug group-hover:text-primary transition-colors duration-300">
              <NuxtLink :to="`/post/${post.id}`">{{ post.title }}</NuxtLink>
            </CardTitle>
          </CardHeader>

          <CardContent class="px-8 py-0 flex-grow">
            <p class="text-muted-foreground/80 font-medium leading-relaxed line-clamp-2">
              {{ post.description }}
            </p>
          </CardContent>

          <CardFooter class="px-8 py-8 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <Avatar class="h-8 w-8 ring-2 ring-background border-2 border-primary/10">
                <AvatarImage :src="post.authorAvatar" />
                <AvatarFallback>{{ post.authorName.charAt(0) }}</AvatarFallback>
              </Avatar>
              <span class="text-sm font-bold opacity-80">{{ post.authorName }}</span>
            </div>
            <NuxtLink :to="`/post/${post.id}`">
                <Button variant="ghost" size="icon" class="rounded-full h-10 w-10 bg-primary/5 text-primary hover:bg-primary hover:text-primary-foreground transition-all duration-300">
                    <LucideArrowRight class="h-5 w-5" />
                </Button>
            </NuxtLink>
          </CardFooter>
        </Card>
      </div>
    </section>

    <!-- Visual Divider -->
    <div class="container px-4 py-24">
        <Separator class="bg-primary/10 h-[2px] rounded-full" />
    </div>

    <!-- Featured Newsletter Card -->
    <section class="container px-4">
        <div class="relative rounded-[3rem] bg-neutral-950 p-12 md:p-24 overflow-hidden group">
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-blue-600/20 via-transparent to-transparent"></div>
            <div class="absolute top-0 right-0 w-[50%] h-[100%] bg-blue-600/10 blur-[120px] rounded-full -mr-[20%] -mt-[20%] transition-transform duration-1000 group-hover:scale-110"></div>
            
            <div class="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-12">
                <div class="max-w-2xl text-center lg:text-left space-y-6">
                    <Badge class="bg-blue-500/10 text-blue-400 border-blue-500/20 px-4 py-1 font-black rounded-lg uppercase tracking-widest text-xs">Stay Informed</Badge>
                    <h2 class="text-4xl md:text-6xl font-black text-white leading-tight">Elevate your <br /> dev knowledge.</h2>
                    <p class="text-xl text-neutral-400 font-medium max-w-xl">Join 15,000+ engineers receiving curated insights on Nuxt, Vue, and the future of web architecture.</p>
                </div>
                
                <div class="w-full max-w-md bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-[2rem] shadow-2xl space-y-4">
                    <div class="space-y-2">
                        <label class="text-sm font-bold text-neutral-400 ml-1">Email Address</label>
                        <Input type="email" placeholder="name@example.com" class="h-14 bg-white/5 border-white/10 text-white placeholder:text-neutral-600 rounded-xl focus:ring-blue-500/50" />
                    </div>
                    <Button size="lg" class="w-full h-14 bg-white text-black hover:bg-neutral-200 text-lg font-black rounded-xl transition-all hover:scale-[1.02] active:scale-95 shadow-xl shadow-white/5">
                        Join the Lab
                    </Button>
                    <p class="text-center text-xs text-neutral-500 font-medium">No spam, just pure engineering. Unsubscribe any time.</p>
                </div>
            </div>
        </div>
    </section>
  </div>
</template>

<script setup>
import { LucideArrowRight, LucideChevronRight } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useBlog } from '~/composables/useBlog'

const { filteredPosts: posts } = useBlog()
</script>
