import { ref, computed } from 'vue'

export interface Post {
    id: number
    title: string
    description: string
    date: string
    readTime: string
    authorName: string
    authorAvatar: string
    category: string
    image: string
}

export const useBlog = () => {
    const posts = ref<Post[]>([
        {
            id: 1,
            title: "Mastering Nuxt 4 Architecture",
            description: "Deep dive into the new directory structure and how to leverage the 'app' directory for better scalability.",
            date: "March 6, 2026",
            readTime: "8 min read",
            authorName: "Alex Rivera",
            authorAvatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
            category: "Architecture",
            image: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&q=80&w=800"
        },
        {
            id: 2,
            title: "The Rise of Utility-First CSS",
            description: "Why Tailwind CSS continues to dominate the industry and how it perfectly complements Shadcn UI.",
            date: "March 5, 2026",
            readTime: "5 min read",
            authorName: "Sarah Chen",
            authorAvatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah",
            category: "Design",
            image: "https://images.unsplash.com/photo-1555066931-4365d1498eb2?auto=format&fit=crop&q=80&w=800"
        },
        {
            id: 3,
            title: "Building Accessible UI Components",
            description: "A guide on using Radix Vue and Shadcn to create components that everyone can use seamlessly.",
            date: "March 4, 2026",
            readTime: "12 min read",
            authorName: "Jordan Smit",
            authorAvatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=Jordan",
            category: "Accessibility",
            image: "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&q=80&w=800"
        }
    ])

    const searchQuery = ref('')
    const selectedCategory = ref('All')

    const categories = computed(() => {
        return ['All', ...new Set(posts.value.map(p => p.category))]
    })

    const filteredPosts = computed(() => {
        return posts.value.filter(post => {
            const matchesSearch = post.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                post.description.toLowerCase().includes(searchQuery.value.toLowerCase())
            const matchesCategory = selectedCategory.value === 'All' || post.category === selectedCategory.value
            return matchesSearch && matchesCategory
        })
    })

    const getPostById = (id: number) => {
        return posts.value.find(p => p.id === id)
    }

    return {
        posts,
        searchQuery,
        selectedCategory,
        categories,
        filteredPosts,
        getPostById
    }
}
