"use client";

import * as z from "zod";
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Loader2, Info, Lightbulb, Plus, Trash2 } from "lucide-react";

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

    // Step 3
    directPersonalData: z.array(z.string()).default([]),
    customDirectData: z.string().optional(),
    collectSensitiveData: z.enum(["yes", "no"]).default("no"),
    sensitiveDataTypes: z.array(z.string()).default([]),
    customSensitiveData: z.string().optional(),
    socialMediaLogin: z.enum(["yes", "no"]).default("no"),
    autoCollectData: z.enum(["yes", "no"]).default("yes"),
    derivativeDataTypes: z.array(z.string()).default([]),
    customAutoCategoryName: z.string().optional(),
    customAutoCategoryDesc: z.string().optional(),
    requestDevicePermissions: z.enum(["yes", "no"]).default("no"),
    requestDeviceStorage: z.enum(["yes", "no"]).default("no"),
    devicePermissionTypes: z.array(z.string()).default([]),
    customDevicePermission: z.string().optional(),
    pushNotifications: z.enum(["yes", "no"]).default("no"),
    googleSync: z.enum(["yes", "no"]).default("no"),
    thirdPartySources: z.enum(["yes", "no"]).default("no"),
    understandTracking: z.boolean().default(false),
    understandSources: z.boolean().default(false),

    // Step 4
    understandLegalBases: z.boolean().default(false),
    processForContract: z.enum(["yes", "no"]).default("no"),
    contractPurposes: z.array(z.string()).default([]),
    processSensitiveForContract: z.enum(["yes", "no"]).default("no"),
    contractSensitiveItems: z.array(z.object({ info: z.string(), desc: z.string() })).default([]),
    processForLegitimate: z.enum(["yes", "no"]).default("no"),
    legitimatePurposes: z.array(z.string()).default([]),
    processSensitiveForLegitimate: z.enum(["yes", "no"]).default("no"),
    legitimateSensitiveItems: z.array(z.object({ reason: z.string(), desc: z.string(), requirement: z.string() })).default([]),
    marketingConsent: z.enum(["yes", "no"]).default("no"),
    marketingSms: z.enum(["yes", "no"]).default("no"),
    marketingMethods: z.array(z.string()).default([]),
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

            directPersonalData: ["names", "phone numbers", "email addresses"],
            collectSensitiveData: "no",
            socialMediaLogin: "no",
            autoCollectData: "yes",
            derivativeDataTypes: ["log and usage data", "device data"],
            customAutoCategoryName: "",
            customAutoCategoryDesc: "",
            requestDevicePermissions: "no",
            requestDeviceStorage: "no",
            pushNotifications: "no",
            googleSync: "no",
            thirdPartySources: "no",
            understandTracking: false,
            understandSources: false,

            understandLegalBases: false,
            processForContract: "no",
            contractPurposes: [],
            processSensitiveForContract: "no",
            contractSensitiveItems: [],
            processForLegitimate: "no",
            legitimatePurposes: [],
            processSensitiveForLegitimate: "no",
            legitimateSensitiveItems: [],
            marketingConsent: "no",
            marketingSms: "no",
            marketingMethods: [],
        },
    });

    const { fields: contractFields, append: appendContract, remove: removeContract } = useFieldArray({
        control: form.control,
        name: "contractSensitiveItems" as const,
    });

    const { fields: legitimateFields, append: appendLegitimate, remove: removeLegitimate } = useFieldArray({
        control: form.control,
        name: "legitimateSensitiveItems" as const,
    });

    const nextStep = () => {
        if (currentStep < 10) {
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
        console.log("Submitting final form values:", values);
        setTimeout(() => {
            setIsLoading(false);
            alert("Step 3 submitted! All data collected.");
        }, 2000);
    }

    return (
        <div className="w-full max-w-3xl mx-auto py-8">
            <div className="mb-8 pl-4 lg:pl-0">
                <h2 className="text-2xl font-extrabold text-slate-900 mb-1 lg:text-3xl">
                    {currentStep === 1 && "Privacy Policy Uses"}
                    {currentStep === 2 && "User Information"}
                    {currentStep === 3 && "Collection of Information"}
                </h2>
                <p className="text-sm text-slate-500 font-semibold tracking-tight">
                    {currentStep === 1 && "What will this Privacy Policy be used for?"}
                    {currentStep === 2 && "User Location"}
                    {currentStep === 3 && "Don't reveal your secrets, just your data."}
                </p>
            </div>

            <Form {...form}>
                <form className="space-y-12">
                    {currentStep === 1 && (
                        <div className="space-y-12">
                            <Card className="border-slate-200 shadow-sm overflow-hidden">
                                <CardHeader className="bg-slate-50/50 border-b py-5 pl-7">
                                    <CardTitle className="text-lg font-bold">Account Verification</CardTitle>
                                    <CardDescription className="text-xs">Verify your credentials before saving changes.</CardDescription>
                                </CardHeader>
                                <CardContent className="pt-8 px-7 space-y-6">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        <FormField control={form.control} name="username" render={({ field }) => (
                                            <FormItem>
                                                <FormLabel className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Username</FormLabel>
                                                <FormControl><Input placeholder="johndoe" {...field} className="bg-slate-50/50 border-slate-200 text-sm h-11" /></FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )} />
                                        <FormField control={form.control} name="password" render={({ field }) => (
                                            <FormItem>
                                                <FormLabel className="text-[10px] font-bold uppercase tracking-widest text-slate-400">Password</FormLabel>
                                                <FormControl><Input type="password" placeholder="••••••••" {...field} className="bg-slate-50/50 border-slate-200 text-sm h-11" /></FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )} />
                                    </div>
                                </CardContent>
                            </Card>

                            <div className="space-y-10 px-4 lg:px-0">
                                <h3 className="font-extrabold text-slate-800 border-b-2 border-slate-100 pb-3 text-lg">What will this Privacy Policy be used for?</h3>
                                <div className="space-y-8">
                                    {[
                                        { name: "website" as const, label: "Website", urlKey: "websiteUrl" as const, urlLabel: "What is the URL address of your website?", desc: "Enter the URL of the website for which you are making this Privacy Policy." },
                                        { name: "mobileApp" as const, label: "Mobile application", urlKey: "mobileAppName" as const, urlLabel: "What is the name of your mobile application?", desc: "Enter the full name of your mobile app." },
                                        { name: "facebookApp" as const, label: "Facebook application", urlKey: "facebookAppName" as const, urlLabel: "What is the name of your Facebook application?", desc: "Enter the full name of your Facebook app." }
                                    ].map((item) => (
                                        <div key={item.name} className="space-y-4">
                                            <FormField control={form.control} name={item.name} render={({ field }) => (
                                                <FormItem className="flex flex-row items-center space-x-3.5 space-y-0">
                                                    <FormControl><Checkbox checked={field.value as boolean} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300 w-5 h-5" /></FormControl>
                                                    <FormLabel className="font-bold text-slate-800 text-[15px]">{item.label}</FormLabel>
                                                </FormItem>
                                            )} />
                                            {form.watch(item.name) && (
                                                <FormField control={form.control} name={item.urlKey} render={({ field }) => (
                                                    <FormItem className="pl-8.5 space-y-2">
                                                        <FormLabel className="text-sm font-bold text-slate-900">{item.urlLabel}</FormLabel>
                                                        <FormDescription className="text-xs text-slate-500 italic pb-1">{item.desc}</FormDescription>
                                                        <FormControl><Input placeholder="e.g., myawesomeproject.com" {...field} className="border-slate-200 text-sm h-11 bg-white/50" /></FormControl>
                                                    </FormItem>
                                                )} />
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}

                    {currentStep === 2 && (
                        <div className="space-y-12 px-4 lg:px-0">
                            <div className="space-y-10">
                                <h3 className="font-extrabold text-slate-800 border-b-2 border-slate-100 pb-3 text-lg">User Location</h3>
                                <div className="space-y-8">
                                    {[
                                        { name: "usersInUS" as const, label: "Do you have users in the United States?" },
                                        { name: "usersInEU" as const, label: "Do you have users in the EU, UK, Switzerland, Iceland, Liechtenstein, or Norway?" },
                                        { name: "usersInCanada" as const, label: "Do you have users in Canada?" }
                                    ].map((item) => (
                                        <FormField key={item.name} control={form.control} name={item.name} render={({ field }) => (
                                            <FormItem className="space-y-4">
                                                <FormLabel className="text-[15px] font-bold text-slate-900">{item.label}</FormLabel>
                                                <FormControl>
                                                    <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" className="w-5 h-5 border-slate-300 text-blue-600" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">Yes</FormLabel></FormItem>
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" className="w-5 h-5 border-slate-300 text-blue-600" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">No</FormLabel></FormItem>
                                                    </RadioGroup>
                                                </FormControl>
                                            </FormItem>
                                        )} />
                                    ))}
                                </div>
                            </div>

                            <div className="space-y-10">
                                <h3 className="font-extrabold text-slate-800 border-b-2 border-slate-100 pb-3 text-lg">User Accounts</h3>
                                <FormField control={form.control} name="canCreateAccount" render={({ field }) => (
                                    <FormItem className="space-y-4">
                                        <FormLabel className="text-[15px] font-bold text-slate-900">Can users create an account or register with your website or app?</FormLabel>
                                        <FormControl>
                                            <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" className="w-5 h-5 border-slate-300" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">Yes</FormLabel></FormItem>
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" className="w-5 h-5 border-slate-300" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">No</FormLabel></FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )} />
                            </div>

                            <div className="space-y-10">
                                <h3 className="font-extrabold text-slate-800 border-b-2 border-slate-100 pb-3 text-lg">User Age</h3>
                                <FormField control={form.control} name="targetMinors" render={({ field }) => (
                                    <FormItem className="space-y-4">
                                        <FormLabel className="text-[15px] font-bold text-slate-900">Do you target users under the age of 18?</FormLabel>
                                        <FormControl>
                                            <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" className="w-5 h-5 border-slate-300" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">Yes</FormLabel></FormItem>
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" className="w-5 h-5 border-slate-300" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">No</FormLabel></FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )} />

                                <div className="pt-6 space-y-5">
                                    <p className="text-[11px] font-extrabold text-slate-500 uppercase tracking-widest">Advanced Options (Not recommended for most users)</p>
                                    <p className="text-[12px] text-slate-400 italic leading-relaxed">The majority of users do not need to change these settings. Consult with a lawyer if unsure.</p>
                                    <FormField control={form.control} name="addCustomMinorLanguage" render={({ field }) => (
                                        <FormItem className="flex flex-row items-center space-x-3.5 space-y-0 pt-2">
                                            <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300 w-5 h-5 rounded" /></FormControl>
                                            <FormLabel className="text-sm font-bold text-slate-800">Add custom language regarding minors</FormLabel>
                                        </FormItem>
                                    )} />
                                    {form.watch("addCustomMinorLanguage") && (
                                        <FormField control={form.control} name="customMinorLanguage" render={({ field }) => (
                                            <FormItem><FormControl><Textarea {...field} className="min-h-[120px] border-slate-200 text-sm resize-none rounded-xl bg-slate-50" /></FormControl></FormItem>
                                        )} />
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {currentStep === 3 && (
                        <div className="space-y-16 px-4 lg:px-0">
                            {/* Collection of Information Intro */}
                            <div className="space-y-6">
                                <h3 className="font-extrabold text-slate-900 text-xl border-b-2 border-slate-100 pb-3">Collection of Information</h3>
                                <p className="text-sm text-slate-500 font-medium">Test an answer in this part what information you collect from users.</p>
                            </div>

                            {/* Personal Information Collected Directly */}
                            <div className="space-y-10">
                                <div className="space-y-2">
                                    <h4 className="font-bold text-slate-800">Personal Information Collected Directly</h4>
                                    <p className="text-[12px] text-slate-500 italic">Please select the personal information components you collect directly from users.</p>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-3 gap-y-5 gap-x-8">
                                    {["names", "phone numbers", "email addresses", "mailing addresses", "job titles", "usernames", "passwords", "contact preferences", "contact or authentication data", "billing addresses", "debit/credit card numbers", "others"].map((val) => (
                                        <FormField key={val} control={form.control} name="directPersonalData" render={({ field }) => (
                                            <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                                <FormControl>
                                                    <Checkbox
                                                        checked={field.value?.includes(val)}
                                                        onCheckedChange={(checked) => {
                                                            return checked
                                                                ? field.onChange([...field.value, val])
                                                                : field.onChange(field.value?.filter((value) => value !== val));
                                                        }}
                                                        className="w-5 h-5 border-slate-300 rounded"
                                                    />
                                                </FormControl>
                                                <FormLabel className="text-sm font-medium text-slate-700 capitalize">{val}</FormLabel>
                                            </FormItem>
                                        )} />
                                    ))}
                                </div>
                                <div className="flex gap-3 pt-2">
                                    <Input placeholder="Enter custom personal information you collect..." className="h-11 border-slate-200 text-sm" />
                                    <Button type="button" size="sm" className="bg-slate-900 text-xs px-6 h-11">+ ADD</Button>
                                </div>
                            </div>

                            {/* Sensitive Personal Information Collected */}
                            <div className="space-y-10">
                                <div className="space-y-2">
                                    <h4 className="font-bold text-slate-800">Sensitive Personal Information Collected</h4>
                                    <p className="text-[12px] text-slate-500 italic">Do you collect sensitive information?</p>
                                </div>
                                <FormField control={form.control} name="collectSensitiveData" render={({ field }) => (
                                    <FormItem className="space-y-4">
                                        <FormControl>
                                            <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">Yes</FormLabel></FormItem>
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">No</FormLabel></FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )} />

                                {form.watch("collectSensitiveData") === "yes" && (
                                    <div className="space-y-8 animate-in fade-in slide-in-from-top-2 duration-300">
                                        <div className="space-y-2">
                                            <p className="text-xs font-bold text-slate-900">Please select the sensitive components you collect:</p>
                                            <p className="text-[11px] text-slate-500">Only the components which are relevant for your business and required by law.</p>
                                        </div>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-y-5 gap-x-8">
                                            {["health data", "financial data", "race or ethnic origin", "religious or philosophical beliefs", "sexual orientation", "genetic or biometric data"].map((val) => (
                                                <FormField key={val} control={form.control} name="sensitiveDataTypes" render={({ field }) => (
                                                    <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                                        <FormControl>
                                                            <Checkbox
                                                                checked={field.value?.includes(val)}
                                                                onCheckedChange={(checked) => {
                                                                    return checked
                                                                        ? field.onChange([...field.value, val])
                                                                        : field.onChange(field.value?.filter((v: string) => v !== val));
                                                                }}
                                                                className="w-5 h-5 border-slate-300 rounded"
                                                            />
                                                        </FormControl>
                                                        <FormLabel className="text-sm font-medium text-slate-700 capitalize">{val}</FormLabel>
                                                    </FormItem>
                                                )} />
                                            ))}
                                        </div>
                                        <div className="flex gap-3">
                                            <Input placeholder="Enter sensitive information components..." className="h-11 border-slate-200 text-sm" />
                                            <Button type="button" size="sm" className="bg-slate-900 text-xs px-6 h-11">+ ADD</Button>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Automated Collection */}
                            <div className="space-y-10">
                                <div className="space-y-2">
                                    <h4 className="font-bold text-slate-800">Personal Information Collected Automatically (Derivative Data)</h4>
                                    <p className="text-[12px] text-slate-500 italic">Will you be collecting derivative data from your users?</p>
                                </div>
                                <FormField control={form.control} name="autoCollectData" render={({ field }) => (
                                    <FormItem className="space-y-4">
                                        <FormControl>
                                            <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">Yes</FormLabel></FormItem>
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">No</FormLabel></FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )} />
                                {form.watch("autoCollectData") === "yes" && (
                                    <div className="space-y-6">
                                        <p className="text-xs font-bold text-slate-800">Please choose categories of derivative data from users for which you collect data:</p>
                                        <div className="space-y-6">
                                            {[
                                                { id: "log", label: "Log and usage data", desc: "Localize log and usage data is service-related, diagnostic, usage and performance information our servers automatically collect when you access or use our Website and which we record in log files." },
                                                { id: "device", label: "Device data", desc: "We collect device data such as information about your computer, phone, tablet or other device you use to access our website. Depending on the device used, this device data can include information such as your IP address." },
                                                { id: "location", label: "Location data", desc: "We collect location data such as information about your device's location, which can be either precise or imprecise. How much information we collect depends on the type and settings of the device you use to access." }
                                            ].map((item) => (
                                                <div key={item.id} className="space-y-3">
                                                    <div className="flex flex-row items-center space-x-3 space-y-0">
                                                        <Checkbox className="w-5 h-5 border-slate-300 rounded" checked={true} disabled />
                                                        <span className="font-bold text-slate-800 text-sm">{item.label}</span>
                                                    </div>
                                                    <p className="pl-8 text-[11px] text-slate-500 leading-relaxed italic">{item.desc}</p>
                                                </div>
                                            ))}
                                        </div>

                                        <div className="space-y-6 pt-6 border-t border-slate-100">
                                            <p className="text-sm font-bold text-slate-900">Do you want to add own category?</p>
                                            <div className="space-y-4">
                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                    <FormField control={form.control} name="customAutoCategoryName" render={({ field }) => (
                                                        <FormItem className="space-y-1.5">
                                                            <FormLabel className="text-[10px] font-bold uppercase text-slate-400">Category Name</FormLabel>
                                                            <FormControl><Input placeholder="e.g., Performance Data" {...field} className="h-10 text-xs border-slate-200" /></FormControl>
                                                        </FormItem>
                                                    )} />
                                                    <FormField control={form.control} name="customAutoCategoryDesc" render={({ field }) => (
                                                        <FormItem className="space-y-1.5">
                                                            <FormLabel className="text-[10px] font-bold uppercase text-slate-400">Category Description</FormLabel>
                                                            <FormControl><Input placeholder="e.g., Load times, crash logs..." {...field} className="h-10 text-xs border-slate-200" /></FormControl>
                                                        </FormItem>
                                                    )} />
                                                </div>
                                                <Button type="button" size="sm" className="bg-slate-900 text-[10px] font-bold tracking-widest px-8 h-10 w-full md:w-auto uppercase">
                                                    + ADD
                                                </Button>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Online Social Network Data */}
                            <div className="space-y-10">
                                <div className="space-y-4">
                                    <h4 className="font-bold text-slate-800">Online Social Network Data</h4>
                                    <p className="text-[12px] text-slate-500 italic leading-relaxed">
                                        If you choose to register an account with us using a third-party account (such as Facebook or Google), we may receive certain profile information about you from the social media provider.
                                    </p>
                                </div>
                                <FormField control={form.control} name="socialMediaLogin" render={({ field }) => (
                                    <FormItem className="space-y-4">
                                        <p className="text-sm font-bold text-slate-900">Will you be requesting any information via social media accounts?</p>
                                        <FormControl>
                                            <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )} />
                                {form.watch("socialMediaLogin") === "yes" && (
                                    <div className="space-y-6 animate-in fade-in slide-in-from-top-2">
                                        <p className="text-xs font-bold text-slate-800">Please select the profile information components you receive:</p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-y-5 gap-x-8">
                                            {["name", "e-mail address", "friends list", "profile picture", "social media bios"].map((val) => (
                                                <div key={val} className="flex flex-row items-start space-x-3 space-y-0">
                                                    <Checkbox className="w-5 h-5 border-slate-300 rounded" checked={true} disabled />
                                                    <span className="text-sm font-medium text-slate-700 capitalize">{val}</span>
                                                </div>
                                            ))}
                                        </div>
                                        <FormField control={form.control} name="googleSync" render={({ field }) => (
                                            <FormItem className="pt-4 flex flex-row items-center space-x-3 space-y-0">
                                                <FormControl><Checkbox checked={field.value === "yes"} onCheckedChange={(c) => field.onChange(c ? "yes" : "no")} className="w-5 h-5 border-slate-300 rounded" /></FormControl>
                                                <FormLabel className="text-sm font-bold text-slate-800">Enable Google Account Synchronization logic?</FormLabel>
                                            </FormItem>
                                        )} />
                                    </div>
                                )}
                            </div>

                            {/* Third-party Sources / Applications */}
                            <div className="space-y-12">
                                <h3 className="font-extrabold text-slate-900 text-lg border-b-2 border-slate-100 pb-3">Personal Information from Applications</h3>

                                <div className="space-y-8">
                                    <div className="space-y-4">
                                        <p className="text-sm font-bold text-slate-900">Will you be requesting access to any user credentials?</p>
                                        <FormField control={form.control} name="socialMediaLogin" render={({ field }) => (
                                            <FormItem>
                                                <FormControl>
                                                    <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                    </RadioGroup>
                                                </FormControl>
                                            </FormItem>
                                        )} />
                                    </div>

                                    <div className="space-y-4">
                                        <p className="text-sm font-bold text-slate-900">Will you be requesting access to features on your users' mobile devices?</p>
                                        <FormField control={form.control} name="requestDevicePermissions" render={({ field }) => (
                                            <FormItem className="space-y-4">
                                                <FormControl>
                                                    <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                    </RadioGroup>
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )} />
                                    </div>

                                    {form.watch("requestDevicePermissions") === "yes" && (
                                        <div className="space-y-6 animate-in fade-in slide-in-from-left-2 transition-all">
                                            <p className="text-sm font-bold text-slate-900">Which features will you be requesting access to?</p>
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-y-5 gap-x-8">
                                                {["Bluetooth", "Calendar", "Camera", "Contacts", "Files", "Microphone", "Phone", "SMS messages", "Reminders", "Sensors", "Storage", "Social media accounts"].map((val) => (
                                                    <FormField key={val} control={form.control} name="devicePermissionTypes" render={({ field }) => (
                                                        <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                                            <FormControl>
                                                                <Checkbox
                                                                    checked={field.value?.includes(val)}
                                                                    onCheckedChange={(checked) => {
                                                                        return checked
                                                                            ? field.onChange([...field.value, val])
                                                                            : field.onChange(field.value?.filter((v: string) => v !== val));
                                                                    }}
                                                                    className="w-5 h-5 border-slate-300 rounded"
                                                                />
                                                            </FormControl>
                                                            <FormLabel className="text-sm font-medium text-slate-700 capitalize">{val}</FormLabel>
                                                        </FormItem>
                                                    )} />
                                                ))}
                                            </div>
                                            <FormField control={form.control} name="customDevicePermission" render={({ field }) => (
                                                <FormItem className="flex gap-3">
                                                    <FormControl><Input placeholder="Enter custom mobile features..." {...field} className="h-11 border-slate-200 text-sm" /></FormControl>
                                                    <Button type="button" size="sm" className="bg-slate-900 text-xs px-6 h-11" onClick={() => field.onChange("")}>+ ADD</Button>
                                                </FormItem>
                                            )} />
                                        </div>
                                    )}

                                    <div className="space-y-4 pt-4">
                                        <p className="text-sm font-bold text-slate-900">Will you be requesting to send you push notifications?</p>
                                        <FormField control={form.control} name="pushNotifications" render={({ field }) => (
                                            <FormItem>
                                                <FormControl>
                                                    <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                        <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                    </RadioGroup>
                                                </FormControl>
                                            </FormItem>
                                        )} />
                                        <p className="text-[11px] text-slate-500 italic leading-relaxed">
                                            Regarding your account or certain features of the app. If you wish to opt-out from receiving these types of communications, you may turn them off in your device's settings.
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Information from other sources */}
                            <div className="space-y-10">
                                <h3 className="font-extrabold text-slate-900 text-lg border-b-2 border-slate-100 pb-3">Information from other sources</h3>
                                <div className="space-y-6">
                                    <p className="text-[12px] text-slate-500 italic leading-relaxed">
                                        In order to enhance our ability to provide relevant marketing, offers, and services to you and update our records, we may obtain information about you from other sources.
                                    </p>
                                    <FormField control={form.control} name="thirdPartySources" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <FormLabel className="text-sm font-bold text-slate-900">Do you collect personal information from other sources?</FormLabel>
                                            <p className="text-[11px] text-slate-400">Such as public databases, joint marketing partners, affiliate programs, data providers, etc.</p>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium text-slate-700">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />
                                </div>
                            </div>

                            {/* Tracking Technologies Section TIPS */}
                            <div className="space-y-10">
                                <div className="bg-amber-50/70 border border-amber-100 p-8 rounded-xl space-y-6">
                                    <div className="flex items-center gap-2">
                                        <Info size={18} className="text-amber-600" />
                                        <h5 className="text-[13px] font-bold text-amber-900">Note on Tracking Technologies:</h5>
                                    </div>
                                    <p className="text-xs text-amber-800 leading-relaxed italic">
                                        We may use cookies and similar tracking technologies (like web beacons and pixels) to access or store information. Specific information about how we use such technologies and how you can refuse certain cookies is set out in our Cookie Notice.
                                    </p>
                                    <FormField control={form.control} name="understandTracking" render={({ field }) => (
                                        <FormItem className="flex flex-row items-start space-x-3 space-y-0 pt-4 border-t border-amber-200/50 mt-4">
                                            <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-amber-600 border-slate-300 w-5 h-5 rounded mt-0.5" /></FormControl>
                                            <FormLabel className="text-xs font-bold text-amber-900 cursor-pointer">Yes, I understand how tracking technologies are used.</FormLabel>
                                        </FormItem>
                                    )} />
                                </div>
                            </div>

                            {/* Other Sources Section with Checklist */}
                            <div className="space-y-10">
                                <div className="bg-blue-50/70 border border-blue-100 p-8 rounded-xl space-y-6">
                                    <div className="flex items-center gap-2">
                                        <Lightbulb size={18} className="text-yellow-500 fill-yellow-500/20" />
                                        <h5 className="text-[13px] font-bold text-blue-900">Tips:</h5>
                                    </div>
                                    <p className="text-xs text-blue-800 leading-relaxed italic">
                                        Under the CCPA and CPRA, other categories of personal information include: publicly available, personal records, financial, medical, etc.
                                    </p>
                                    <p className="text-xs text-blue-800 leading-relaxed italic font-medium">
                                        If you indicate that you collect personal information from other sources, you must list the names of the third parties you collect the information from and why the information collected from them is relevant to your business.
                                    </p>

                                    <FormField control={form.control} name="understandSources" render={({ field }) => (
                                        <FormItem className="flex flex-row items-start space-x-3 space-y-0 pt-4 border-t border-blue-200/50 mt-4">
                                            <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300 w-5 h-5 rounded mt-0.5" /></FormControl>
                                            <FormLabel className="text-xs font-bold text-blue-900 cursor-pointer">Yes, I understand and acknowledge the above.</FormLabel>
                                        </FormItem>
                                    )} />
                                </div>
                            </div>
                        </div>
                    )}

                    {currentStep === 4 && (
                        <div className="space-y-12 animate-in fade-in slide-in-from-right-4 duration-500">
                            {/* Step 4 Header */}
                            <div className="space-y-2">
                                <div className="flex items-center gap-2 mb-1">
                                    <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm">4</div>
                                    <h2 className="text-2xl font-black text-slate-900 tracking-tight">Use of Information</h2>
                                </div>
                                <p className="text-slate-500 text-sm font-medium">How you process your users' personal info</p>
                            </div>

                            {/* EU/UK Legal Bases */}
                            <div className="space-y-8">
                                <h3 className="font-extrabold text-slate-900 text-lg border-b-2 border-slate-100 pb-3">EU/UK Legal Bases for Processing</h3>
                                <div className="space-y-6">
                                    <p className="text-sm font-bold text-slate-900">Which are legal bases for processing a user's personal information?</p>
                                    <p className="text-[12px] text-slate-500 italic leading-relaxed">
                                        When we process any experience in personal information, you must have a valid legal reason for doing so under legal bases. Legal bases for vary under different privacy law.
                                    </p>

                                    <div className="bg-blue-50/70 border border-blue-200 p-6 rounded-xl space-y-4">
                                        <p className="text-[11px] text-blue-800 leading-relaxed font-medium italic">
                                            Under the EU and UK GDPR, you must only process personal information when you have a valid "legal base". There are six lawful bases for processing under the GDPR: Consent, Performance of the Contract, Legal Basis Interest, Legal Obligation, Vital Interest, or Public Task.
                                        </p>
                                    </div>

                                    <div className="bg-amber-50/70 border border-amber-200 p-6 rounded-xl space-y-4">
                                        <p className="text-[11px] text-amber-800 leading-relaxed font-medium italic">
                                            Unless you comply with GDPR, you must not default into your privacy policy with only legal bases: Performance of a contract.
                                        </p>
                                        <p className="text-[11px] text-amber-800 leading-relaxed font-medium italic">
                                            In this following page, you will be asked to select the reasons why you process information in the context of these legal bases.
                                        </p>
                                    </div>

                                    <div className="bg-yellow-50/70 border border-yellow-200 p-6 rounded-xl space-y-4">
                                        <p className="text-[11px] text-yellow-800 leading-relaxed font-medium italic">
                                            Infinite privacy policy uses legal bases under the GDPR:
                                        </p>
                                        <p className="text-[11px] text-yellow-800 leading-relaxed font-medium italic">
                                            By default, your Privacy Policy states that processing is necessary to provide the services under your contract with the user (Performance of Contract). However, in specific situations, you can justify other legal bases. Please select carefully any reasons that you choose to use in the context of these legal bases.
                                        </p>
                                    </div>

                                    <FormField control={form.control} name="understandLegalBases" render={({ field }) => (
                                        <FormItem className="flex flex-row items-start space-x-3 space-y-0 pt-4 border-t border-slate-100">
                                            <FormControl><Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300 w-5 h-5 rounded mt-0.5" /></FormControl>
                                            <FormLabel className="text-xs font-bold text-slate-700 cursor-pointer">Yes, I understand the Terms that identify legal bases for default in the privacy policy.</FormLabel>
                                        </FormItem>
                                    )} />
                                </div>
                            </div>

                            {/* Provision of Services */}
                            <div className="space-y-8">
                                <h3 className="font-extrabold text-slate-900 text-lg border-b-2 border-slate-100 pb-3 uppercase tracking-tighter">Legal Basis: Provision of Services / Performance of a Contract</h3>
                                <div className="space-y-6">
                                    <FormField control={form.control} name="processForContract" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <FormLabel className="text-sm font-bold text-slate-900">Do you process user information to provide your Services / fulfill needs related to a Contract with them?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    {form.watch("processForContract") === "yes" && (
                                        <FormField control={form.control} name="contractPurposes" render={({ field }) => (
                                            <FormItem className="space-y-4 animate-in fade-in slide-in-from-left-2 transition-all">
                                                <p className="text-xs font-bold text-slate-800">We will process your personal information for these purposes depending on how you interact with our website, then you should select each:</p>
                                                <div className="space-y-3">
                                                    {[
                                                        "To deliver and facilitate the delivery of services to the user",
                                                        "To enable user-to-user communications",
                                                        "To fulfill and manage your orders",
                                                        "To respond to user inquiries",
                                                        "To send administrative information to users"
                                                    ].map((val) => (
                                                        <FormItem key={val} className="flex flex-row items-center space-x-3 space-y-0">
                                                            <FormControl>
                                                                <Checkbox
                                                                    checked={field.value?.includes(val)}
                                                                    onCheckedChange={(checked) => {
                                                                        return checked
                                                                            ? field.onChange([...field.value, val])
                                                                            : field.onChange(field.value?.filter((v: string) => v !== val));
                                                                    }}
                                                                    className="w-5 h-5 border-slate-300"
                                                                />
                                                            </FormControl>
                                                            <FormLabel className="text-sm font-medium text-slate-700">{val}</FormLabel>
                                                        </FormItem>
                                                    ))}
                                                </div>
                                            </FormItem>
                                        )} />
                                    )}

                                    <FormField control={form.control} name="processSensitiveForContract" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <FormLabel className="text-sm font-bold text-slate-900">Do you process any sensitive user personal information?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    {form.watch("processSensitiveForContract") === "yes" && (
                                        <div className="space-y-6 pt-4 border-t border-slate-100 animate-in fade-in slide-in-from-left-2 transition-all">
                                            <p className="text-xs text-slate-500 italic font-medium leading-relaxed">
                                                Provide details on why processing user sensitive personal information is a business requirement.
                                            </p>
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                <div className="space-y-1.5">
                                                    <label className="text-[10px] font-bold uppercase text-slate-400">Specific Information</label>
                                                    <Input id="contractInfo" placeholder="e.g., Financial Data" className="h-10 text-xs border-slate-200" />
                                                </div>
                                                <div className="space-y-1.5">
                                                    <label className="text-[10px] font-bold uppercase text-slate-400">Description</label>
                                                    <Input id="contractDesc" placeholder="e.g., To process billing and payments." className="h-10 text-xs border-slate-200" />
                                                </div>
                                            </div>
                                            <Button
                                                type="button"
                                                size="sm"
                                                className="bg-slate-900 text-[10px] font-bold tracking-widest px-8 h-10 w-full md:w-auto uppercase"
                                                onClick={() => {
                                                    const info = (document.getElementById("contractInfo") as HTMLInputElement).value;
                                                    const desc = (document.getElementById("contractDesc") as HTMLInputElement).value;
                                                    if (info && desc) {
                                                        appendContract({ info, desc });
                                                        (document.getElementById("contractInfo") as HTMLInputElement).value = "";
                                                        (document.getElementById("contractDesc") as HTMLInputElement).value = "";
                                                    }
                                                }}
                                            >
                                                + ADD
                                            </Button>

                                            {contractFields.length > 0 && (
                                                <div className="space-y-3">
                                                    {contractFields.map((field, index) => (
                                                        <div key={field.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                                                            <div className="flex flex-col">
                                                                <span className="text-xs font-bold text-slate-800">{field.info}</span>
                                                                <span className="text-[10px] text-slate-500">{field.desc}</span>
                                                            </div>
                                                            <Button type="button" variant="ghost" size="sm" onClick={() => removeContract(index)}>
                                                                <Trash2 size={14} className="text-red-500" />
                                                            </Button>
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Legitimate Interests */}
                            <div className="space-y-8">
                                <h3 className="font-extrabold text-slate-900 text-lg border-b-2 border-slate-100 pb-3 uppercase tracking-tighter">Legal Basis: Legitimate Interests</h3>
                                <div className="space-y-6">
                                    <FormField control={form.control} name="processForLegitimate" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <FormLabel className="text-sm font-bold text-slate-900">Are there any other legitimate reasons why you process users' information?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    {form.watch("processForLegitimate") === "yes" && (
                                        <div className="space-y-6 animate-in fade-in slide-in-from-left-2 transition-all">
                                            <div className="bg-blue-50/70 border border-blue-200 p-6 rounded-xl">
                                                <p className="text-[11px] text-blue-800 leading-relaxed font-medium italic">
                                                    Legitimate interests may apply as legal basis in cases when processing personal information in ways that represent minimal impact on users' rights and interests, such those for computing just basis for processing. As such, you must evaluate that impacts on your users' rights and interests by conducting Legitimate Interest Assessment (LIA).
                                                </p>
                                            </div>

                                            <FormField control={form.control} name="legitimatePurposes" render={({ field }) => (
                                                <FormItem className="space-y-4">
                                                    <div className="space-y-3">
                                                        {[
                                                            { id: "adv", label: "To deliver targeted advertising to users", sub: "to serve advertisements relevant to user based on user behavior, browsing activity, past visit etc." },
                                                            { id: "promo", label: "To determine the effectiveness of promotional campaigns", sub: "in order to measure your marketing success." },
                                                            { id: "trends", label: "To identify usage trends", sub: "in order to distinguish users and learn how users use our products they you can improve them and user experience." },
                                                            { id: "protect", label: "To protect user accounts", sub: "in order to identify and prevent potential account safety threats through systems." },
                                                            { id: "feedback", label: "To support feedback", sub: "in order to understand how your users interact with your products/services as such you can improve user experience." },
                                                            { id: "market", label: "To send user marketing and promotional communications", sub: "in order to evaluate and update our update and improve our customer and prospect contact records." },
                                                            { id: "enforce", label: "To enforce our terms, conditions and policies for business purposes, to comply with legal and regulatory requirements or in connection with our contract.", sub: "" }
                                                        ].map((item) => (
                                                            <FormItem key={item.id} className="flex flex-row items-start space-x-3 space-y-0">
                                                                <FormControl>
                                                                    <Checkbox
                                                                        checked={field.value?.includes(item.label)}
                                                                        onCheckedChange={(checked) => {
                                                                            return checked
                                                                                ? field.onChange([...field.value, item.label])
                                                                                : field.onChange(field.value?.filter((v: string) => v !== item.label));
                                                                        }}
                                                                        className="w-5 h-5 border-slate-300 rounded mt-0.5"
                                                                    />
                                                                </FormControl>
                                                                <div className="space-y-1">
                                                                    <FormLabel className="text-sm font-bold text-slate-800">{item.label}</FormLabel>
                                                                    {item.sub && <p className="text-[10px] text-slate-500 italic">{item.sub}</p>}
                                                                </div>
                                                            </FormItem>
                                                        ))}
                                                    </div>
                                                </FormItem>
                                            )} />

                                            <FormField control={form.control} name="processSensitiveForLegitimate" render={({ field }) => (
                                                <FormItem className="space-y-4 pt-4 border-t border-slate-100">
                                                    <FormLabel className="text-sm font-bold text-slate-900">Do you process sensitive personal information because you believe it represents a legitimate interest?</FormLabel>
                                                    <FormControl>
                                                        <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                            <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                            <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                        </RadioGroup>
                                                    </FormControl>
                                                </FormItem>
                                            )} />

                                            {form.watch("processSensitiveForLegitimate") === "yes" && (
                                                <div className="space-y-6 pt-4 animate-in fade-in slide-in-from-left-2 transition-all">
                                                    <p className="text-xs text-slate-500 italic font-medium leading-relaxed">
                                                        Please state the reason for using this information, describe those reasons and state why this use is legally mandated for selection.
                                                    </p>
                                                    <div className="space-y-4">
                                                        <div className="space-y-1.5">
                                                            <label className="text-[10px] font-bold uppercase text-slate-400">Reason for using information</label>
                                                            <Input id="legitReason" placeholder="e.g., Security Monitoring" className="h-10 text-xs border-slate-200" />
                                                        </div>
                                                        <div className="space-y-1.5">
                                                            <label className="text-[10px] font-bold uppercase text-slate-400">Description</label>
                                                            <Input id="legitDesc" placeholder="e.g., Monitoring for suspicious activity..." className="h-10 text-xs border-slate-200" />
                                                        </div>
                                                        <div className="space-y-1.5">
                                                            <label className="text-[10px] font-bold uppercase text-slate-400">Legal requirement status</label>
                                                            <Input id="legitReq" placeholder="e.g., Compliance with AML statutes" className="h-10 text-xs border-slate-200" />
                                                        </div>
                                                    </div>
                                                    <Button
                                                        type="button"
                                                        size="sm"
                                                        className="bg-slate-900 text-[10px] font-bold tracking-widest px-8 h-10 w-full md:w-auto uppercase"
                                                        onClick={() => {
                                                            const reason = (document.getElementById("legitReason") as HTMLInputElement).value;
                                                            const desc = (document.getElementById("legitDesc") as HTMLInputElement).value;
                                                            const requirement = (document.getElementById("legitReq") as HTMLInputElement).value;
                                                            if (reason && desc && requirement) {
                                                                appendLegitimate({ reason, desc, requirement });
                                                                (document.getElementById("legitReason") as HTMLInputElement).value = "";
                                                                (document.getElementById("legitDesc") as HTMLInputElement).value = "";
                                                                (document.getElementById("legitReq") as HTMLInputElement).value = "";
                                                            }
                                                        }}
                                                    >
                                                        + ADD
                                                    </Button>

                                                    {legitimateFields.length > 0 && (
                                                        <div className="space-y-3">
                                                            {legitimateFields.map((field, index) => (
                                                                <div key={field.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-200">
                                                                    <div className="flex flex-col">
                                                                        <span className="text-xs font-bold text-slate-800">{field.reason}</span>
                                                                        <span className="text-[10px] text-slate-500">{field.desc}</span>
                                                                        <span className="text-[9px] text-slate-400 italic">Legal: {field.requirement}</span>
                                                                    </div>
                                                                    <Button type="button" variant="ghost" size="sm" onClick={() => removeLegitimate(index)}>
                                                                        <Trash2 size={14} className="text-red-500" />
                                                                    </Button>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>

                            {/* Marketing and Promotional Communications */}
                            <div className="space-y-8">
                                <h3 className="font-extrabold text-slate-900 text-lg border-b-2 border-slate-100 pb-3">Marketing and Promotional Communications</h3>
                                <div className="space-y-6">
                                    <FormField control={form.control} name="marketingConsent" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <FormLabel className="text-sm font-bold text-slate-900">Do you send marketing and promotional communications to your users?</FormLabel>
                                            <p className="text-[11px] text-slate-400 italic">We may process the personal information you send to us for our marketing purposes, if this is in accordance with your preferences.</p>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    <FormField control={form.control} name="marketingSms" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <FormLabel className="text-sm font-bold text-slate-900">Do you use SMS messaging to market users?</FormLabel>
                                            <FormControl>
                                                <RadioGroup onValueChange={field.onChange} defaultValue={field.value} className="flex flex-col space-y-2.5">
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="yes" /></FormControl><FormLabel className="text-sm font-medium">Yes</FormLabel></FormItem>
                                                    <FormItem className="flex items-center space-x-3.5 space-y-0"><FormControl><RadioGroupItem value="no" /></FormControl><FormLabel className="text-sm font-medium">No</FormLabel></FormItem>
                                                </RadioGroup>
                                            </FormControl>
                                        </FormItem>
                                    )} />

                                    <div className="bg-yellow-50/70 border border-yellow-200 p-6 rounded-xl">
                                        <p className="text-[11px] text-yellow-800 leading-relaxed font-medium italic">
                                            If a consumer chooses to opt out, you must honor at person's choice within 10 business days. It is common for business to use several avenues of person to opt out. The items below represent some of the avenues common to business services.
                                        </p>
                                    </div>

                                    <FormField control={form.control} name="marketingMethods" render={({ field }) => (
                                        <FormItem className="space-y-4">
                                            <p className="text-sm font-bold text-slate-900">How do users communicate preferences from our communications?</p>
                                            <div className="space-y-3">
                                                {[
                                                    "Clicking the checkbox that's in the bottom of our marketing emails",
                                                    "Ticking 'I accept marketing communications'",
                                                    "Joining mailing list through Third-party partner",
                                                    "By Asking Consumer directly by mail/sms"
                                                ].map((val) => (
                                                    <div key={val} className="flex flex-row items-center space-x-3 space-y-0">
                                                        <Checkbox
                                                            checked={field.value?.includes(val)}
                                                            onCheckedChange={(checked) => {
                                                                return checked
                                                                    ? field.onChange([...field.value, val])
                                                                    : field.onChange(field.value?.filter((v: string) => v !== val));
                                                            }}
                                                            className="w-5 h-5 border-slate-300"
                                                        />
                                                        <span className="text-sm font-medium text-slate-700">{val}</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </FormItem>
                                    )} />

                                    <div className="space-y-4 pt-4 border-t border-slate-100">
                                        <p className="text-sm font-bold text-slate-900">Will you use:</p>
                                        <div className="flex gap-3">
                                            <Input placeholder="e.g., WhatsApp, Push notifications..." className="h-11 border-slate-200 text-sm" />
                                            <Button type="button" size="sm" className="bg-slate-900 text-xs px-6 h-11 uppercase">+ ADD</Button>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Final Step 4 Tips */}
                            <div className="space-y-10">
                                <div className="bg-blue-50/70 border border-blue-100 p-8 rounded-xl space-y-6">
                                    <div className="flex items-center gap-2">
                                        <Info size={18} className="text-blue-600" />
                                        <h5 className="text-[13px] font-bold text-blue-900">Tips:</h5>
                                    </div>
                                    <p className="text-[11px] text-blue-800 leading-relaxed font-bold">
                                        Compliance matters!
                                    </p>
                                    <p className="text-[11px] text-blue-800 leading-relaxed italic">
                                        Ensure your use of legal bases matches the GDPR's intended use to avoid legal complex with your policy.
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Persistent Navigation Buttons */}
                    <div className="flex items-center justify-between pt-10 border-t border-slate-100">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={prevStep}
                            disabled={currentStep === 1 || isLoading}
                            className="border-slate-200 text-slate-600 hover:bg-slate-50 min-w-[120px] h-11 font-bold text-xs uppercase tracking-widest"
                        >
                            ← Back
                        </Button>
                        <div className="flex items-center gap-4">
                            <Button type="button" variant="ghost" className="text-slate-500 hover:text-slate-900 px-8 font-bold text-xs uppercase tracking-widest">
                                Save
                            </Button>
                            <Button
                                type="button"
                                onClick={nextStep}
                                disabled={isLoading}
                                className="bg-slate-900 hover:bg-slate-800 text-white min-w-[120px] h-11 font-bold text-xs uppercase tracking-widest transition-all shadow-md"
                            >
                                {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : currentStep === 10 ? "Submit" : "Next →"}
                            </Button>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}
