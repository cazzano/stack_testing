"use client";

import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { ShieldCheck, LayoutGrid, FileText, CheckCircle2, ChevronRight, Twitter, Linkedin, Github, Mail } from "lucide-react";
import Link from "next/link";

export function Header() {
    return (
        <header className="border-b bg-white sticky top-0 z-50">
            <div className="container mx-auto px-4 h-16 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-600 rounded-md flex items-center justify-center text-white">
                        <ShieldCheck size={20} />
                    </div>
                    <div>
                        <h1 className="font-bold text-slate-900 leading-tight">Privacy Policy Builder</h1>
                        <p className="text-[10px] text-blue-600 font-medium">Privacy Pilot</p>
                    </div>
                </div>

                <nav className="hidden md:flex items-center gap-6">
                    <Link href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600">Policy Builder</Link>
                    <Link href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600">Templates</Link>
                    <Link href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600">Policies</Link>
                    <Link href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600">Compliance Guide</Link>
                    <Link href="#" className="text-sm font-medium text-slate-600 hover:text-blue-600">Pricing</Link>
                </nav>

                <div className="flex items-center gap-4">
                    <Button size="sm" className="bg-slate-900 hover:bg-slate-800 text-white font-semibold">
                        Start Building
                    </Button>
                </div>
            </div>
        </header>
    );
}

const steps = [
    { id: 1, title: "Privacy Policy Uses", status: "completed", desc: "What will this Privacy Policy be used for?" },
    { id: 2, title: "User Information", status: "todo", desc: "User Location" },
    { id: 3, title: "Collection of Information", status: "todo", desc: "Personal Information Collected Directly" },
    { id: 4, title: "Use of Information", status: "todo", desc: "How do we process your information?" },
    { id: 5, title: "Disclosure of Information", status: "todo", desc: "When and with whom do we share your personal information?" },
    { id: 6, title: "Use of Tracking Technologies", status: "todo", desc: "Do we use cookies and other tracking technologies?" },
    { id: 7, title: "User Rights", status: "todo", desc: "What are your privacy rights?" },
    { id: 8, title: "Final Details", status: "todo", desc: "Review Your Policy Coverage" },
];

export function Sidebar() {
    return (
        <aside className="w-80 border-r bg-slate-50/50 min-h-[calc(100vh-64px)] p-6 overflow-y-auto hidden lg:block">
            <div className="mb-8">
                <h2 className="text-sm font-bold text-slate-900 mb-2 uppercase tracking-wider">Progress</h2>
                <div className="flex items-center gap-3">
                    <Progress value={12} className="h-2 flex-1" />
                    <span className="text-xs font-semibold text-slate-500">1 of 8 completed</span>
                </div>
            </div>

            <div className="space-y-3">
                {steps.map((step) => (
                    <div
                        key={step.id}
                        className={`flex gap-4 p-3 rounded-xl border transition-all cursor-pointer ${step.id === 1 ? "bg-white border-blue-100 shadow-sm" : "bg-transparent border-transparent hover:bg-slate-100/50"
                            }`}
                    >
                        <div className={`w-8 h-8 shrink-0 rounded-full flex items-center justify-center text-xs font-bold border ${step.id === 1 ? "bg-blue-600 border-blue-600 text-white" : "bg-slate-200 border-slate-200 text-slate-500"
                            }`}>
                            {step.id}
                        </div>
                        <div className="flex flex-col gap-0.5">
                            <h3 className={`text-xs font-bold ${step.id === 1 ? "text-blue-900" : "text-slate-700"}`}>{step.title}</h3>
                            <p className="text-[10px] text-slate-500 leading-relaxed max-w-[180px]">{step.desc}</p>
                        </div>
                    </div>
                ))}
            </div>
        </aside>
    );
}

export function Footer() {
    return (
        <footer className="bg-[#0f172a] text-slate-400 py-12">
            <div className="container mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
                    <div className="col-span-1">
                        <div className="flex items-center gap-2 mb-4">
                            <div className="w-8 h-8 bg-blue-600 rounded-md flex items-center justify-center text-white">
                                <ShieldCheck size={20} />
                            </div>
                            <h2 className="text-white font-bold text-lg">Privacy Pilot</h2>
                        </div>
                        <p className="text-sm leading-relaxed mb-6">
                            Generate professional, compliant privacy policies with our intelligent wizard. Trusted by thousands of businesses worldwide.
                        </p>
                        <div className="flex gap-4">
                            <Link href="#" className="hover:text-blue-400 transition-colors"><Twitter size={18} /></Link>
                            <Link href="#" className="hover:text-blue-400 transition-colors"><Linkedin size={18} /></Link>
                            <Link href="#" className="hover:text-blue-400 transition-colors"><Github size={18} /></Link>
                            <Link href="#" className="hover:text-blue-400 transition-colors"><Mail size={18} /></Link>
                        </div>
                    </div>

                    <div>
                        <h3 className="text-white font-bold mb-6">Product</h3>
                        <ul className="space-y-4 text-sm">
                            <li><Link href="#" className="hover:text-white transition-colors">Policy Builder</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Templates</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Compliance Guide</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Pricing</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-white font-bold mb-6">Resources</h3>
                        <ul className="space-y-4 text-sm">
                            <li><Link href="#" className="hover:text-white transition-colors">Documentation</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Blog</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Case Studies</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Help Center</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-white font-bold mb-6">Company</h3>
                        <ul className="space-y-4 text-sm">
                            <li><Link href="#" className="hover:text-white transition-colors">About Us</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Contact</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                            <li><Link href="#" className="hover:text-white transition-colors">Terms of Service</Link></li>
                        </ul>
                    </div>
                </div>

                <Separator className="bg-slate-800 mb-8" />

                <div className="flex flex-col md:flex-row justify-between items-center gap-4 text-xs font-medium">
                    <p>© 2024 Privacy Pilot. All rights reserved.</p>
                    <p>Built with ❤️ for privacy compliance</p>
                </div>
            </div>
        </footer>
    );
}
