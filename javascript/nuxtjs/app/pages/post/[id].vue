<template>
  <div v-if="post" class="relative pb-32">
    <!-- Progress Bar (Client Side Only) -->
    <div class="fixed top-0 left-0 h-1 bg-primary z-[60] transition-all duration-300" :style="{ width: `${scrollProgress}%` }"></div>

    <!-- Header / Hero -->
    <header class="relative pt-16 pb-24 md:pt-24 md:pb-32 overflow-hidden">
        <div class="absolute inset-0 bg-primary/5 -z-10"></div>
        <div class="absolute top-0 right-0 w-full h-full bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent opacity-50"></div>
        
        <div class="container px-4 max-w-4xl">
            <NuxtLink to="/articles" class="group inline-flex items-center gap-2 text-sm font-bold text-muted-foreground hover:text-primary transition-colors mb-12">
                <div class="p-2 rounded-lg bg-background shadow-sm border group-hover:bg-primary group-hover:text-primary-foreground transition-all">
                    <LucideArrowLeft class="h-4 w-4" />
                </div>
                Back to Articles
            </NuxtLink>

            <div class="space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-1000">
                <div class="flex flex-wrap items-center gap-3">
                    <Badge class="bg-primary/10 text-primary border-primary/20 px-4 py-1 font-black rounded-lg uppercase tracking-widest text-xs">
                        {{ post.category }}
                    </Badge>
                    <span class="text-sm font-bold text-muted-foreground/60 uppercase tracking-widest">{{ post.readTime }}</span>
                </div>
                
                <h1 class="text-4xl md:text-6xl font-black tracking-tight leading-[1.1] text-balance">
                    {{ post.title }}
                </h1>

                <div class="flex items-center gap-4 pt-4">
                    <Avatar class="h-12 w-12 ring-4 ring-background shadow-xl">
                        <AvatarImage :src="post.authorAvatar" />
                        <AvatarFallback>{{ post.authorName.charAt(0) }}</AvatarFallback>
                    </Avatar>
                    <div class="flex flex-col">
                        <span class="font-black text-lg leading-none">{{ post.authorName }}</span>
                        <span class="text-sm font-bold text-muted-foreground/80 mt-1">{{ post.date }}</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <div class="container px-4 max-w-4xl -mt-12">
        <!-- Main Image -->
        <div class="relative aspect-[16/9] md:aspect-[21/9] rounded-[2.5rem] overflow-hidden shadow-2xl border-8 border-background animate-in fade-in zoom-in duration-1000 delay-300">
            <img :src="post.image" :alt="post.title" class="object-cover w-full h-full transform hover:scale-105 transition-transform duration-1000" />
        </div>

        <!-- Article Content -->
        <article class="mt-16 prose prose-neutral dark:prose-invert max-w-none">
            <div class="space-y-12 animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-500">
                <p class="text-xl md:text-2xl leading-relaxed font-medium text-muted-foreground italic border-l-4 border-primary pl-8 py-2">
                    "{{ post.description }}"
                </p>

                <div class="space-y-6 text-lg md:text-xl leading-relaxed text-muted-foreground font-medium">
                    <p>
                        In the rapidly evolving landscape of web development, staying ahead means mastering not just the tools, but the architectural philosophies that drive them. Nuxt 4 represents a significant leap forward in how we conceptualize and build universal Vue applications.
                    </p>
                    
                    <h2 class="text-3xl font-black text-foreground tracking-tight pt-8">The Core Proposition</h2>
                    <p>
                        One of the most striking features of this era is the emphasis on Developer Experience (DX) without compromising on User Experience (UX). By leveraging the "app" directory pattern, we can now structure our applications with unprecedented clarity.
                    </p>

                    <div class="my-12 p-8 md:p-12 bg-muted/40 border-y md:border-x md:rounded-[2rem] border-primary/10 relative overflow-hidden group">
                        <div class="absolute top-0 right-0 p-4 opacity-5 transform group-hover:scale-110 transition-transform">
                            <LucidePentagon class="h-32 w-32 text-primary" />
                        </div>
                        <h3 class="text-2xl font-black mb-6 text-foreground">Key Strategic Takeaways</h3>
                        <ul class="space-y-4 m-0 p-0 list-none">
                            <li v-for="(item, i) in ['Seamless hydration patterns', 'Predictive route prefetching', 'Advanced middle-layer orchestration', 'Atomic design integration']" :key="i" class="flex items-start gap-3">
                                <div class="mt-1.5 h-2 w-2 rounded-full bg-primary shadow-sm shadow-primary/40 shrink-0"></div>
                                <span class="font-bold text-foreground/80">{{ item }}</span>
                            </li>
                        </ul>
                    </div>

                    <p>
                        We also need to consider the visual layer. Shadcn UI isn't just a component library; it's a testament to the power of accessible, headless UI primitives. When combined with the utility-first philosophy of Tailwind CSS, the speed of iteration becomes almost gravity-defying.
                    </p>
                </div>
            </div>
        </article>

        <!-- Dynamic Author Section -->
        <Separator class="my-20" />
        
        <div class="p-8 md:p-12 rounded-[2.5rem] bg-background border shadow-[0_20px_50px_-15px_rgba(0,0,0,0.05)] flex flex-col md:flex-row items-center gap-10">
            <Avatar class="h-32 w-32 ring-8 ring-muted/20 shadow-2xl shrink-0">
                <AvatarImage :src="post.authorAvatar" />
                <AvatarFallback>{{ post.authorName.charAt(0) }}</AvatarFallback>
            </Avatar>
            <div class="space-y-4 text-center md:text-left">
                <div class="space-y-1">
                    <h3 class="text-2xl font-black tracking-tight">Written by {{ post.authorName }}</h3>
                    <p class="text-sm font-bold uppercase tracking-widest text-primary">Senior Architecture Lead</p>
                </div>
                <p class="text-muted-foreground font-medium leading-relaxed max-w-xl">
                    {{ post.authorName }} has been pioneering digital architecture for over a decade, with a focus on building resilient, accessible, and high-performance web ecosystems.
                </p>
                <div class="flex justify-center md:justify-start gap-4 pt-2">
                    <Button variant="outline" size="sm" class="rounded-xl font-bold border-primary/20 transition-all hover:bg-primary hover:text-primary-foreground">
                        Follow on Twitter
                    </Button>
                    <Button variant="ghost" size="sm" class="rounded-xl font-bold">
                        View Profile
                    </Button>
                </div>
            </div>
        </div>
    </div>
  </div>
  
  <div v-else class="h-[80vh] flex flex-col items-center justify-center space-y-8">
      <div class="h-24 w-24 bg-muted rounded-full flex items-center justify-center animate-pulse">
        <LucidePentagon class="h-12 w-12 text-muted-foreground" />
      </div>
      <h1 class="text-3xl font-black">Decrypting Post...</h1>
      <NuxtLink to="/articles">
          <Button variant="outline" class="rounded-xl font-bold">Return Home</Button>
      </NuxtLink>
  </div>
</template>

<script setup>
import { LucideArrowLeft, LucidePentagon } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { useRoute } from 'vue-router'
import { useBlog } from '~/composables/useBlog'
import { ref, onMounted, onUnmounted } from 'vue'

const route = useRoute()
const { getPostById } = useBlog()
const post = getPostById(Number(route.params.id))

const scrollProgress = ref(0)
const handleScroll = () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = (window.pageYOffset / totalHeight) * 100
    scrollProgress.value = progress
}

onMounted(() => {
    window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
})
</script>
