import { LoginForm } from "@/components/login-form";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24 bg-slate-50 dark:bg-slate-950">
      <LoginForm />
    </main>
  );
}
