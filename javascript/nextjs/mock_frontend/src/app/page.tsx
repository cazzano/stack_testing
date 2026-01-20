"use client";

import { useState } from "react";
import { Header, Sidebar, Footer } from "@/components/layout-components";
import { LoginForm } from "@/components/login-form";

export default function Home() {
  const [currentStep, setCurrentStep] = useState(1);

  return (
    <div className="flex flex-col min-h-screen bg-slate-50 dark:bg-slate-950">
      <Header />

      <div className="flex flex-1 container mx-auto px-4 gap-8">
        <Sidebar currentStep={currentStep} />

        <main className="flex-1 min-w-0 py-6 md:py-12">
          <div className="max-w-4xl mx-auto">
            <LoginForm onStepChange={(step) => setCurrentStep(step)} />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}
