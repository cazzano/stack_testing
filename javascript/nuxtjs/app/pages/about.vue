<template>
  <div class="relative overflow-hidden pb-32">
    <!-- Fluid background elements -->
    <div class="absolute top-0 left-[20%] w-[60%] h-[600px] bg-primary/5 blur-[120px] -z-10 rounded-full"></div>
    <div class="absolute top-1/2 -right-[10%] w-[40%] h-[600px] bg-blue-500/5 blur-[120px] -z-10 rounded-full"></div>

    <div class="container px-4 pt-20 md:pt-32">
      <div class="space-y-32">
        <!-- Hero Section -->
        <section class="max-w-4xl mx-auto text-center space-y-8 animate-in fade-in slide-in-from-bottom-8 duration-1000">
          <Badge variant="outline" class="px-4 py-1.5 text-xs font-black uppercase tracking-[0.2em] bg-primary text-primary-foreground border-transparent rounded-lg shadow-lg shadow-primary/20">
            About Antigravity
          </Badge>
          <h1 class="text-5xl md:text-8xl font-black tracking-tighter leading-[0.95] text-balance">
            We're on a mission to <span class="text-transparent bg-clip-text bg-gradient-to-br from-blue-600 via-indigo-500 to-purple-600">redefine the web.</span>
          </h1>
          <p class="text-xl md:text-2xl text-muted-foreground/80 leading-relaxed font-medium max-w-3xl mx-auto">
            Antigravity is an engineering-first publication focused on the intersection of advanced web architecture, high-performance UI, and the future of human-computer interaction.
          </p>
        </section>

        <!-- Vision Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
          <div class="space-y-8 animate-in fade-in slide-in-from-left-12 duration-1000 delay-300">
            <h2 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">Our Vision of Nuxt 4 & Beyond</h2>
            <div class="space-y-6 text-xl text-muted-foreground/90 font-medium leading-relaxed">
                <p>
                We believe that the next generation of web applications will be characterized by extreme performance, seamless accessibility, and a meticulous attention to design detail.
                </p>
                <p>
                By deep-diving into the evolving ecosystem of Nuxt 4, Tailwind CSS, and Shadcn, we aim to provide the tactical knowledge required to build world-class digital products.
                </p>
            </div>
            <div class="flex gap-4 pt-4">
                <div class="flex flex-col">
                    <span class="text-4xl font-black text-primary">15k+</span>
                    <span class="text-sm font-bold uppercase tracking-widest text-muted-foreground">Engineers</span>
                </div>
                <Separator orientation="vertical" class="h-12 mx-4" />
                <div class="flex flex-col">
                    <span class="text-4xl font-black text-primary">200+</span>
                    <span class="text-sm font-bold uppercase tracking-widest text-muted-foreground">Insights</span>
                </div>
            </div>
          </div>
          <div class="relative group animate-in fade-in slide-in-from-right-12 duration-1000 delay-500">
            <div class="absolute inset-0 bg-gradient-to-br from-primary to-purple-600 rounded-[3rem] blur-2xl opacity-20 group-hover:opacity-30 transition-opacity"></div>
            <div class="relative aspect-square md:aspect-video lg:aspect-square rounded-[3rem] overflow-hidden shadow-2xl border-4 border-background ring-1 ring-primary/10">
                <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=1200" alt="Team working" class="object-cover w-full h-full transform transition-transform duration-1000 group-hover:scale-110" />
                <div class="absolute inset-0 bg-gradient-to-t from-primary/40 to-transparent"></div>
            </div>
          </div>
        </div>

        <!-- Topics Grid -->
        <section class="space-y-16">
            <div class="text-center space-y-4">
                <h2 class="text-4xl md:text-5xl font-black tracking-tight">Core Disciplines</h2>
                <p class="text-xl text-muted-foreground font-medium">The pillars of our editorial strategy</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                <Card v-for="(topic, index) in topics" :key="topic.title" 
                      class="relative p-8 rounded-[2.5rem] border-none bg-background shadow-[0_10px_40px_-15px_rgba(0,0,0,0.1)] hover:shadow-[0_20px_60px_-15px_rgba(0,0,0,0.15)] transition-all duration-500 hover:-translate-y-2 group overflow-hidden animate-in fade-in zoom-in duration-700"
                      :style="{ transitionDelay: `${index * 100}ms` }">
                    <div class="absolute top-0 right-0 p-4 opacity-5 transform group-hover:scale-150 group-hover:opacity-10 transition-all duration-700">
                        <component :is="topic.icon" class="h-24 w-24 text-primary" />
                    </div>
                    <div class="relative z-10 space-y-4">
                        <div class="h-14 w-14 rounded-2xl bg-primary/10 flex items-center justify-center text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground duration-500">
                            <component :is="topic.icon" class="h-7 w-7" />
                        </div>
                        <h3 class="font-black text-2xl tracking-tight">{{ topic.title }}</h3>
                        <p class="text-muted-foreground/80 font-medium leading-relaxed">{{ topic.description }}</p>
                    </div>
                </Card>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="relative rounded-[3rem] bg-primary p-12 md:p-24 text-primary-foreground overflow-hidden text-center space-y-10 group">
            <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/10 to-transparent"></div>
            <div class="absolute -top-24 -left-24 w-64 h-64 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-1000"></div>
            
            <div class="relative z-10 space-y-6 max-w-2xl mx-auto">
                <h2 class="text-4xl md:text-6xl font-black tracking-tighter">Become a part <br /> of our journey.</h2>
                <p class="text-xl md:text-2xl font-medium opacity-90 leading-relaxed">
                    Join a community of forward-thinking engineers and designers building the next generation of the web.
                </p>
            </div>
            <div class="relative z-10 flex flex-col sm:flex-row justify-center gap-6">
                <Button size="lg" variant="secondary" class="h-16 px-12 text-xl font-black rounded-2xl shadow-xl transition-all hover:scale-105 active:scale-95">
                    Join the Lab
                </Button>
                <Button size="lg" variant="outline" class="h-16 px-12 text-xl font-black rounded-2xl border-white/20 hover:bg-white/10 transition-all">
                    Our Twitter
                </Button>
            </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { LucideLayout, LucideCpu, LucideLayers, LucideAccessibility, LucideZap, LucideShieldCheck } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'
import { Separator } from '@/components/ui/separator'
import { Button } from '@/components/ui/button'

const topics = [
    { title: "Architecture", description: "Mastering the foundations of modern web apps.", icon: LucideLayers },
    { title: "DX", description: "Streamlining developer workflows and tools.", icon: LucideZap },
    { title: "Design Systems", description: "Scaling UI with consistency and speed.", icon: LucideLayout },
    { title: "Accessibility", description: "Building an inclusive web for everyone.", icon: LucideAccessibility },
    { title: "Performance", description: "Optimizing for speed and efficiency.", icon: LucideCpu },
    { title: "Security", description: "Protecting data and user privacy.", icon: LucideShieldCheck },
]
</script>
