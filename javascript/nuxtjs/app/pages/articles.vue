<template>
  <div class="relative min-h-screen pb-24">
    <!-- Background Accents -->
    <div class="absolute top-0 right-0 w-[50%] h-[500px] bg-primary/5 blur-[120px] -z-10 rounded-full"></div>
    <div class="absolute bottom-0 left-0 w-[30%] h-[400px] bg-purple-500/5 blur-[100px] -z-10 rounded-full"></div>

    <div class="container px-4 pt-16 md:pt-24">
      <!-- Header Section -->
      <div class="flex flex-col gap-8 mb-16">
        <div class="space-y-4 max-w-3xl">
          <Badge variant="outline" class="px-4 py-1.5 text-xs font-black uppercase tracking-widest bg-primary/5 text-primary border-primary/20 rounded-lg">
            Knowledge Base
          </Badge>
          <h1 class="text-5xl md:text-6xl font-black tracking-tight leading-[1.1]">
            Curated <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Articles</span>
          </h1>
          <p class="text-xl text-muted-foreground/80 font-medium leading-relaxed">
            Deep dives, tutorials, and strategic insights from the forefront of web engineering.
          </p>
        </div>

        <div class="flex flex-col sm:flex-row gap-6 items-start sm:items-center justify-between border-b pb-8">
            <div class="flex flex-wrap gap-2">
                <Button 
                    v-for="category in categories" 
                    :key="category"
                    :variant="selectedCategory === category ? 'default' : 'outline'"
                    size="sm"
                    class="rounded-xl px-6 font-bold h-10 transition-all active:scale-95"
                    @click="selectedCategory = category"
                >
                    {{ category }}
                </Button>
            </div>
            <div class="text-sm font-bold text-muted-foreground bg-muted/30 px-4 py-2 rounded-lg border">
                Showing {{ posts.length }} Articles
            </div>
        </div>
      </div>

      <!-- Articles Grid -->
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div v-for="n in 6" :key="n" class="space-y-6">
          <Skeleton class="aspect-[16/9] rounded-[1.5rem]" />
          <div class="space-y-3">
            <Skeleton class="h-4 w-[100px]" />
            <Skeleton class="h-8 w-full" />
            <Skeleton class="h-4 w-full" />
            <Skeleton class="h-4 w-2/3" />
          </div>
          <div class="flex items-center gap-3 pt-4 border-t">
            <Skeleton class="h-8 w-8 rounded-full" />
            <Skeleton class="h-4 w-[100px]" />
          </div>
        </div>
      </div>

      <div v-else-if="posts.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <Card v-for="(post, index) in posts" :key="post.id" 
              class="group flex flex-col h-full border-none bg-background/40 backdrop-blur-sm border border-primary/5 shadow-sm hover:shadow-2xl transition-all duration-500 rounded-[2rem] overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700"
              :style="{ transitionDelay: `${index * 100}ms` }">
          
          <NuxtLink :to="`/post/${post.id}`" class="block aspect-[16/9] relative overflow-hidden m-3 rounded-[1.5rem]">
            <img :src="post.image" :alt="post.title" class="object-cover w-full h-full transform transition-transform duration-700 group-hover:scale-110" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="absolute top-4 left-4">
                <Badge class="bg-white/90 backdrop-blur text-black border-none font-bold rounded-lg">{{ post.category }}</Badge>
            </div>
          </NuxtLink>

          <CardHeader class="px-6 pt-3">
            <div class="flex items-center gap-2 text-xs font-bold text-muted-foreground/60 tracking-widest uppercase mb-2">
              <span>{{ post.date }}</span>
              <span class="w-1 h-1 rounded-full bg-primary/30"></span>
              <span>{{ post.readTime }}</span>
            </div>
            <CardTitle class="text-[1.35rem] font-black leading-tight group-hover:text-primary transition-colors duration-300">
              <NuxtLink :to="`/post/${post.id}`">{{ post.title }}</NuxtLink>
            </CardTitle>
          </CardHeader>

          <CardContent class="px-6 py-0 flex-grow">
            <p class="text-muted-foreground font-medium leading-relaxed line-clamp-3 text-sm">
              {{ post.description }}
            </p>
          </CardContent>

          <CardFooter class="px-6 py-6 mt-4 flex items-center justify-between border-t bg-muted/5">
              <div class="flex items-center gap-2.5">
                <Avatar class="h-7 w-7 ring-2 ring-background border border-primary/10">
                    <AvatarImage :src="post.authorAvatar" />
                    <AvatarFallback>{{ post.authorName.charAt(0) }}</AvatarFallback>
                </Avatar>
                <span class="text-xs font-bold opacity-70">{{ post.authorName }}</span>
              </div>
              <NuxtLink :to="`/post/${post.id}`">
                <Button variant="ghost" size="sm" class="font-bold text-primary hover:bg-primary/10 transition-colors">
                    Read Article
                </Button>
              </NuxtLink>
          </CardFooter>
        </Card>
      </div>
      
      <!-- Empty State -->
      <div v-else class="py-40 text-center space-y-8 animate-in fade-in zoom-in duration-500">
          <div class="h-24 w-24 bg-primary/5 rounded-full flex items-center justify-center mx-auto border border-primary/10 shadow-inner">
              <LucideSearchX class="h-12 w-12 text-primary" />
          </div>
          <div class="space-y-2">
            <h2 class="text-3xl font-black">No articles found</h2>
            <p class="text-lg text-muted-foreground font-medium max-w-sm mx-auto">We couldn't find any articles matching your current search or category filters.</p>
          </div>
          <Button variant="outline" size="lg" class="rounded-xl px-10 font-bold h-12 border-primary/20" @click="resetFilters">
              Reset all filters
          </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { LucideSearchX } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Skeleton } from '@/components/ui/skeleton'
import { useBlog } from '~/composables/useBlog'
import { ref, watch } from 'vue'

const { filteredPosts: posts, categories, selectedCategory, searchQuery } = useBlog()
const isLoading = ref(false)

// Simulate loading when filters change
watch([selectedCategory, searchQuery], () => {
    isLoading.value = true
    setTimeout(() => {
        isLoading.value = false
    }, 400)
})

const resetFilters = () => {
    selectedCategory.value = 'All'
    searchQuery.value = ''
}
</script>
