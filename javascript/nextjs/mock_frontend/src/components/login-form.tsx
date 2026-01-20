"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Loader2, Info, Lightbulb } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Textarea } from "@/components/ui/textarea";

const formSchema = z.object({
    // Step 1
    username: z.string().min(2, { message: "Username must be at least 2 characters." }),
    password: z.string().min(8, { message: "Password must be at least 8 characters." }),
    website: z.boolean().default(false),
    websiteUrl: z.string().optional(),
    mobileApp: z.boolean().default(false),
    mobileAppName: z.string().optional(),
    facebookApp: z.boolean().default(false),
    facebookAppName: z.string().optional(),
    englishPreference: z.enum(["american", "british"]).default("american"),
    includeDescription: z.enum(["yes", "no"]).default("yes"),
    productDescription: z.string().optional(),
    productName: z.string().optional(),

    // Step 2
    usersInUS: z.enum(["yes", "no"]).default("yes"),
    usersInEU: z.enum(["yes", "no"]).default("yes"),
    usersInCanada: z.enum(["yes", "no"]).default("yes"),
    canCreateAccount: z.enum(["yes", "no"]).default("no"),
    targetMinors: z.enum(["yes", "no"]).default("no"),
    addCustomMinorLanguage: z.boolean().default(false),
    customMinorLanguage: z.string().optional(),
});

interface LoginFormProps {
    onStepChange?: (step: number) => void;
}

export function LoginForm({ onStepChange }: LoginFormProps) {
    const [currentStep, setCurrentStep] = useState(1);
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "luca_dev",
            password: "password123",
            website: true,
            websiteUrl: "cazzano.vercel.app",
            mobileApp: true,
            mobileAppName: "Logfile App",
            facebookApp: true,
            facebookAppName: "Advita App",
            englishPreference: "american",
            includeDescription: "yes",
            productName: "Resource management",
            productDescription: "It will automatically manages the important resources of your device to the right things.",

            usersInUS: "yes",
            usersInEU: "yes",
            usersInCanada: "yes",
            canCreateAccount: "no",
            targetMinors: "no",
            addCustomMinorLanguage: false,
            customMinorLanguage: "Our app is designed for minors under 18 and includes appropriate content safeguards.",
        },
    });

    const nextStep = () => {
        if (currentStep < 2) {
            setCurrentStep(prev => {
                const next = prev + 1;
                onStepChange?.(next);
                return next;
            });
            window.scrollTo(0, 0);
        } else {
            form.handleSubmit(onSubmit)();
        }
    };

    const prevStep = () => {
        setCurrentStep(prev => {
            const next = prev - 1;
            onStepChange?.(next);
            return next;
        });
        window.scrollTo(0, 0);
    };

    function onSubmit(values: z.infer<typeof formSchema>) {
        setIsLoading(true);
        console.log("Submitting form values:", values);
        setTimeout(() => {
            setIsLoading(false);
            alert("All steps submitted successfully!");
        }, 2000);
    }

    return (
        <div className="w-full max-w-2xl mx-auto py-8">
            <div className="mb-8">
                <h2 className="text-2xl font-bold text-slate-900 mb-1">
                    {currentStep === 1 ? "Privacy Policy Uses" : "User Information"}
                </h2>
                <p className="text-sm text-slate-500 font-medium">
                    {currentStep === 1 ? "What will this Privacy Policy be used for?" : "User Location"}
                </p>
            </div>

            <Form {...form}>
                <form className="space-y-12">
                    {currentStep === 1 && (
                        <>
                            {/* Step 1 Content (Previous implementation) */}
                            <Card className="border-slate-200 shadow-sm">
                                <CardHeader className="bg-slate-50/50 border-b py-4">
                                    <CardTitle className="text-lg">Account Verification</CardTitle>
                                    <CardDescription>Verify your credentials before saving changes.</CardDescription>
                                </CardHeader>
                                <CardContent className="pt-6 space-y-4">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <FormField control={form.control} name="username" render={({ field }) => (
                                            <FormItem>
                                                <FormLabel className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Username</FormLabel>
                                                <FormControl><Input placeholder="johndoe" {...field} className="bg-slate-50 border-slate-200 text-sm" /></FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )} />
                                        <FormField control={form.control} name="password" render={({ field }) => (
                                            <FormItem>
                                                <FormLabel className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Password</FormLabel>
                                                <FormControl><Input type="password" placeholder="••••••••" {...field} className="bg-slate-50 border-slate-200 text-sm" /></FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )} />
                                    </div>
                                </CardContent>
                            </Card>

                            <div className="space-y-8">
                                <h3 className="font-bold text-slate-800 border-b pb-2">What will this Privacy Policy be used for?</h3>
                                <div className="space-y-6 text-sm">
                                    <div className="space-y-3">
                                        <FormField control={form.control} name="website" render={({ field }) => (
                                            <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                                                <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300" /></FormControl>
                                                <FormLabel className="font-bold text-slate-800">Website</FormLabel>
                                            </FormItem>
                                        )} />
                                        {form.watch("website") && (
                                            <FormField control={form.control} name="websiteUrl" render={({ field }) => (
                                                <FormItem className="pl-7 space-y-1.5">
                                                    <FormLabel className="text-xs font-bold text-slate-900">What is the URL address of your website?</FormLabel>
                                                    <FormDescription className="text-[11px] text-slate-500 italic">Enter the URL of the website for which you are making this Privacy Policy.</FormDescription>
                                                    <FormControl><Input placeholder="e.g., cazzano.vercel.app" {...field} className="border-slate-200 text-sm h-10" /></FormControl>
                                                </FormItem>
                                            )} />
                                        )}
                                    </div>
                                    <div className="space-y-3">
                                        <FormField control={form.control} name="mobileApp" render={({ field }) => (
                                            <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                                                <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300" /></FormControl>
                                                <FormLabel className="font-bold text-slate-800">Mobile application</FormLabel>
                                            </FormItem>
                                        )} />
                                        {form.watch("mobileApp") && (
                                            <FormField control={form.control} name="mobileAppName" render={({ field }) => (
                                                <FormItem className="pl-7 space-y-1.5">
                                                    <FormLabel className="text-xs font-bold text-slate-900 flex items-center gap-1.5">What is the name of your mobile application? <Info size={14} className="text-blue-500" /></FormLabel>
                                                    <FormControl><Input placeholder="e.g., Logfile App" {...field} className="border-slate-200 text-sm h-10" /></FormControl>
                                                </FormItem>
                                            )} />
                                        )}
                                    </div>
                                </div>

                                <div className="space-y-4 pt-4">
                                    <h4 className="font-bold text-slate-900">English Preference</h4>
                                    <FormField control={form.control} name="englishPreference" render={({ field }) => (
                                        <FormItem className="space-y-3">
                                            <FormLabel className="text-xs font-bold text-slate-600">What type of English spelling do you want to be used in this Privacy Policy?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2">
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="american" /></FormControl><FormLabel className="text-xs font-bold text-slate-700">American English</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="british" /></FormControl><FormLabel className="text-xs font-bold text-slate-700">British English</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />
                                </div>

                                <div className="bg-blue-50/70 border border-blue-100 p-6 rounded-xl space-y-2.5">
                                    <h5 className="text-xs font-bold text-blue-700 uppercase tracking-widest">Tips:</h5>
                                    <p className="text-xs text-blue-800 leading-relaxed italic">Certain words will be spelled differently depending on if you are using American English or British English.</p>
                                </div>
                            </div>
                        </>
                    )}

                    {currentStep === 2 && (
                        <>
                            {/* Step 2 Content (NEW based on image) */}
                            <div className="space-y-10">
                                <div className="space-y-6">
                                    <h3 className="font-bold text-slate-800 border-b pb-2">User Location</h3>

                                    {/* Location Radios */}
                                    <FormField control={form.control} name="usersInUS" render={({ field }) => (
                                        <FormItem className="space-y-3">
                                            <FormLabel className="text-[13px] font-bold text-slate-900">Do you have users in the United States?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2">
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-xs font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-xs font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    <FormField control={form.control} name="usersInEU" render={({ field }) => (
                                        <FormItem className="space-y-3">
                                            <FormLabel className="text-[13px] font-bold text-slate-900">Do you have users in the EU, UK, Switzerland, Iceland, Liechtenstein, or Norway?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2">
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-xs font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-xs font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    <FormField control={form.control} name="usersInCanada" render={({ field }) => (
                                        <FormItem className="space-y-3">
                                            <FormLabel className="text-[13px] font-bold text-slate-900">Do you have users in Canada?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2">
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-xs font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-xs font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />
                                </div>

                                <div className="space-y-6">
                                    <h3 className="font-bold text-slate-800 border-b pb-2">User Accounts</h3>
                                    <FormField control={form.control} name="canCreateAccount" render={({ field }) => (
                                        <FormItem className="space-y-3">
                                            <FormLabel className="text-[13px] font-bold text-slate-900">Can users create an account or register with your website or app?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2">
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-xs font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-xs font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />
                                </div>

                                <div className="space-y-6">
                                    <h3 className="font-bold text-slate-800 border-b pb-2">User Age</h3>
                                    <FormField control={form.control} name="targetMinors" render={({ field }) => (
                                        <FormItem className="space-y-3">
                                            <FormLabel className="text-[13px] font-bold text-slate-900">Do you target users under the age of 18?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2">
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-xs font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-xs font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    <div className="pt-4 space-y-4">
                                        <p className="text-xs font-bold text-slate-600 uppercase tracking-tight">Advanced Options (Not recommended for most users)</p>
                                        <p className="text-[11px] text-slate-500 italic leading-relaxed">
                                            The majority of users do not need to change these settings. By interacting with this section, you understand that you should carefully review the resulting policy text and consult with a lawyer before making any changes.
                                        </p>

                                        <FormField control={form.control} name="addCustomMinorLanguage" render={({ field }) => (
                                            <FormItem className="flex flex-row items-center space-x-3 space-y-0 pt-2">
                                                <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300 rounded" /></FormControl>
                                                <FormLabel className="text-xs font-bold text-slate-800">Add custom language regarding minors</FormLabel>
                                            </FormItem>
                                        )} />

                                        {form.watch("addCustomMinorLanguage") && (
                                            <FormField control={form.control} name="customMinorLanguage" render={({ field }) => (
                                                <FormItem>
                                                    <FormControl><Textarea {...field} className="min-h-[100px] border-slate-200 text-sm resize-none rounded-lg" placeholder="Enter your custom language regarding minors..." /></FormControl>
                                                </FormItem>
                                            )} />
                                        )}
                                    </div>
                                </div>

                                {/* Step 2 Tips */}
                                <div className="bg-blue-50/70 border border-blue-100 p-8 rounded-xl space-y-6">
                                    <div className="flex items-center gap-2">
                                        <Lightbulb size={18} className="text-yellow-500 fill-yellow-500/20" />
                                        <h5 className="text-[13px] font-bold text-blue-900">Tips:</h5>
                                    </div>

                                    <div className="space-y-4">
                                        <p className="text-xs font-bold text-blue-800">Users can be internal or external users. They can be external or internal.</p>

                                        <div className="space-y-4 pl-2">
                                            <p className="text-xs font-bold text-blue-800">External users include individuals who:</p>
                                            <ul className="list-disc pl-5 text-xs text-blue-800 space-y-2">
                                                <li>Browse your website</li>
                                                <li>Interact with your website</li>
                                                <li>Use your software/program/platform</li>
                                                <li>Purchase goods or services through your website</li>
                                            </ul>
                                        </div>

                                        <div className="space-y-4 pl-2">
                                            <p className="text-xs font-bold text-blue-800">Internal users include:</p>
                                            <ul className="list-disc pl-5 text-xs text-blue-800 space-y-2 font-medium">
                                                <li>Employees</li>
                                                <li>Managers</li>
                                                <li>Internal auditors</li>
                                            </ul>
                                        </div>

                                        <div className="pt-4 border-t border-blue-200/50">
                                            <p className="text-xs font-bold text-blue-900 mb-2">Note for targeting users under 18:</p>
                                            <p className="text-[11px] text-blue-800 leading-relaxed italic">
                                                When targeting minors, ensure compliance with COPPA (Children's Online Privacy Protection Act) and other applicable regulations. Consider implementing additional safeguards and parental consent mechanisms.
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </>
                    )}

                    {/* Navigation Buttons */}
                    <div className="flex items-center justify-between pt-8 border-t">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={prevStep}
                            disabled={currentStep === 1 || isLoading}
                            className="border-slate-200 text-slate-600 hover:bg-slate-50 min-w-[100px]"
                        >
                            ← Back
                        </Button>
                        <div className="flex items-center gap-3">
                            <Button type="button" variant="ghost" className="text-slate-600 hover:text-slate-900 px-6">
                                Save
                            </Button>
                            <Button
                                type="button"
                                onClick={nextStep}
                                disabled={isLoading}
                                className="bg-slate-900 hover:bg-slate-800 text-white min-w-[100px]"
                            >
                                {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : currentStep === 2 ? "Submit" : "Next →"}
                            </Button>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}
