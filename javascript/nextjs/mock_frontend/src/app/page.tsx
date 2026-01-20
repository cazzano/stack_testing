import { Header, Sidebar, Footer } from "@/components/layout-components";
import { LoginForm } from "@/components/login-form";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-slate-50 dark:bg-slate-950">
      <Header />

      <div className="flex flex-1 container mx-auto px-4 gap-8">
        <Sidebar />

        <main className="flex-1 min-w-0 py-6 md:py-12">
          <div className="max-w-4xl mx-auto">
            <LoginForm />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}
