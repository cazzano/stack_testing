"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Loader2, Info } from "lucide-react";

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
});

export function LoginForm() {
    const [isLoading, setIsLoading] = useState(false);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: "",
            password: "",
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
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        setIsLoading(true);
        console.log("Submitting form values:", values);
        setTimeout(() => {
            setIsLoading(false);
            alert("Form submitted successfully!");
        }, 2000);
    }

    return (
        <div className="w-full max-w-2xl mx-auto py-8">
            <div className="mb-8">
                <h2 className="text-2xl font-bold text-slate-900 mb-1">Privacy Policy Uses</h2>
                <p className="text-sm text-slate-500 font-medium">What will this Privacy Policy be used for?</p>
            </div>

            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-12">
                    {/* Account Verification Section */}
                    <Card className="border-slate-200 shadow-sm">
                        <CardHeader className="bg-slate-50/50 border-b py-4">
                            <CardTitle className="text-lg">Account Verification</CardTitle>
                            <CardDescription>Verify your credentials before saving changes.</CardDescription>
                        </CardHeader>
                        <CardContent className="pt-6 space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <FormField
                                    control={form.control}
                                    name="username"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Username</FormLabel>
                                            <FormControl>
                                                <Input placeholder="johndoe" {...field} className="bg-slate-50 border-slate-200 text-sm" />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                                <FormField
                                    control={form.control}
                                    name="password"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Password</FormLabel>
                                            <FormControl>
                                                <Input type="password" placeholder="••••••••" {...field} className="bg-slate-50 border-slate-200 text-sm" />
                                            </FormControl>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            </div>
                        </CardContent>
                    </Card>

                    {/* Policy Context Section */}
                    <div className="space-y-8">
                        <h3 className="font-bold text-slate-800 border-b pb-2">What will this Privacy Policy be used for?</h3>

                        <div className="space-y-6 text-sm">
                            {/* Website */}
                            <div className="space-y-3">
                                <FormField
                                    control={form.control}
                                    name="website"
                                    render={({ field }) => (
                                        <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                                            <FormControl>
                                                <Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300" />
                                            </FormControl>
                                            <FormLabel className="font-bold text-slate-800">Website</FormLabel>
                                        </FormItem>
                                    )}
                                />
                                {form.watch("website") && (
                                    <FormField
                                        control={form.control}
                                        name="websiteUrl"
                                        render={({ field }) => (
                                            <FormItem className="pl-7 space-y-1.5">
                                                <FormLabel className="text-xs font-bold text-slate-900">What is the URL address of your website?</FormLabel>
                                                <FormDescription className="text-[11px] text-slate-500 italic">Enter the URL of the website for which you are making this Privacy Policy.</FormDescription>
                                                <FormControl>
                                                    <Input placeholder="e.g., cazzano.vercel.app" {...field} className="border-slate-200 text-sm h-10" />
                                                </FormControl>
                                            </FormItem>
                                        )}
                                    />
                                )}
                            </div>

                            {/* Mobile App */}
                            <div className="space-y-3">
                                <FormField
                                    control={form.control}
                                    name="mobileApp"
                                    render={({ field }) => (
                                        <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                                            <FormControl>
                                                <Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300" />
                                            </FormControl>
                                            <FormLabel className="font-bold text-slate-800">Mobile application</FormLabel>
                                        </FormItem>
                                    )}
                                />
                                {form.watch("mobileApp") && (
                                    <FormField
                                        control={form.control}
                                        name="mobileAppName"
                                        render={({ field }) => (
                                            <FormItem className="pl-7 space-y-1.5">
                                                <FormLabel className="text-xs font-bold text-slate-900 flex items-center gap-1.5 cursor-help">
                                                    What is the name of your mobile application? <Info size={14} className="text-blue-500" />
                                                </FormLabel>
                                                <FormDescription className="text-[11px] text-slate-500 italic">Enter the full name of your mobile app.</FormDescription>
                                                <FormControl>
                                                    <Input placeholder="e.g., Logfile App" {...field} className="border-slate-200 text-sm h-10" />
                                                </FormControl>
                                            </FormItem>
                                        )}
                                    />
                                )}
                            </div>

                            {/* Facebook App */}
                            <div className="space-y-3">
                                <FormField
                                    control={form.control}
                                    name="facebookApp"
                                    render={({ field }) => (
                                        <FormItem className="flex flex-row items-center space-x-3 space-y-0">
                                            <FormControl>
                                                <Checkbox checked={field.value} onCheckedChange={field.onChange} className="data-[state=checked]:bg-blue-600 border-slate-300" />
                                            </FormControl>
                                            <FormLabel className="font-bold text-slate-800">Facebook application</FormLabel>
                                        </FormItem>
                                    )}
                                />
                                {form.watch("facebookApp") && (
                                    <FormField
                                        control={form.control}
                                        name="facebookAppName"
                                        render={({ field }) => (
                                            <FormItem className="pl-7 space-y-1.5">
                                                <FormLabel className="text-xs font-bold text-slate-900">What is the name of your Facebook application?</FormLabel>
                                                <FormDescription className="text-[11px] text-slate-500 italic">Enter the full name of your Facebook app.</FormDescription>
                                                <FormControl>
                                                    <Input placeholder="e.g., Advita App" {...field} className="border-slate-200 text-sm h-10" />
                                                </FormControl>
                                            </FormItem>
                                        )}
                                    />
                                )}
                            </div>
                        </div>

                        {/* English Preference */}
                        <div className="space-y-4 pt-4">
                            <h4 className="font-bold text-slate-900">English Preference</h4>
                            <FormField
                                control={form.control}
                                name="englishPreference"
                                render={({ field }) => (
                                    <FormItem className="space-y-3">
                                        <FormLabel className="text-xs font-bold text-slate-600">What type of English spelling do you want to be used in this Privacy Policy?</FormLabel>
                                        <FormControl>
                                            <RadioGroup
                                                onValueChange={field.onChange}
                                                defaultValue={field.value}
                                                className="flex flex-col space-y-2"
                                            >
                                                <FormItem className="flex items-center space-x-3 space-y-0">
                                                    <FormControl>
                                                        <RadioGroupItem value="american" className="border-slate-300 text-blue-600" />
                                                    </FormControl>
                                                    <FormLabel className="text-xs font-bold text-slate-700">American English</FormLabel>
                                                </FormItem>
                                                <FormItem className="flex items-center space-x-3 space-y-0">
                                                    <FormControl>
                                                        <RadioGroupItem value="british" className="border-slate-300 text-blue-600" />
                                                    </FormControl>
                                                    <FormLabel className="text-xs font-bold text-slate-700">British English</FormLabel>
                                                </FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )}
                            />
                        </div>

                        <div className="bg-blue-50/70 border border-blue-100 p-6 rounded-xl space-y-2.5">
                            <h5 className="text-xs font-bold text-blue-700 uppercase tracking-widest">Tips:</h5>
                            <p className="text-xs text-blue-800 leading-relaxed italic">
                                Certain words will be spelled differently depending on if you are using American English or British English. For example, words that end in <span className="font-mono bg-blue-100/50 px-1">-or</span> in American English, typically end in <span className="font-mono bg-blue-100/50 px-1">-our</span> in British English.
                            </p>
                            <p className="text-xs text-blue-800 leading-relaxed italic">
                                There are several words used in this Privacy Policy that would be spelled differently (e.g., behavior – behaviour; personalized – personalised; fulfill – fulfil).
                            </p>
                        </div>

                        {/* Use and Description */}
                        <div className="space-y-8 pt-6">
                            <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
                                Use and Description
                            </h4>

                            <FormField
                                control={form.control}
                                name="includeDescription"
                                render={({ field }) => (
                                    <FormItem className="space-y-3">
                                        <FormLabel className="text-xs font-bold text-slate-600 flex items-center gap-1.5">
                                            Do you want to include a description about your product or service? <Info size={14} className="text-blue-500 cursor-help" />
                                        </FormLabel>
                                        <FormControl>
                                            <RadioGroup
                                                onValueChange={field.onChange}
                                                defaultValue={field.value}
                                                className="flex flex-col space-y-2"
                                            >
                                                <FormItem className="flex items-center space-x-3 space-y-0">
                                                    <FormControl>
                                                        <RadioGroupItem value="yes" className="border-slate-300 text-blue-600" />
                                                    </FormControl>
                                                    <FormLabel className="text-xs font-bold text-slate-700">Yes</FormLabel>
                                                </FormItem>
                                                <FormItem className="flex items-center space-x-3 space-y-0">
                                                    <FormControl>
                                                        <RadioGroupItem value="no" className="border-slate-300 text-blue-600" />
                                                    </FormControl>
                                                    <FormLabel className="text-xs font-bold text-slate-700">No</FormLabel>
                                                </FormItem>
                                            </RadioGroup>
                                        </FormControl>
                                    </FormItem>
                                )}
                            />

                            {form.watch("includeDescription") === "yes" && (
                                <div className="space-y-6">
                                    <FormField
                                        control={form.control}
                                        name="productName"
                                        render={({ field }) => (
                                            <FormItem className="space-y-1.5">
                                                <FormLabel className="text-xs font-bold text-slate-900">Enter a description of your product or service:</FormLabel>
                                                <FormControl>
                                                    <Input {...field} className="border-slate-200 text-sm h-10" />
                                                </FormControl>
                                            </FormItem>
                                        )}
                                    />
                                    <FormField
                                        control={form.control}
                                        name="productDescription"
                                        render={({ field }) => (
                                            <FormItem className="space-y-1.5">
                                                <FormControl>
                                                    <Textarea {...field} className="min-h-[100px] border-slate-200 text-sm resize-none" />
                                                </FormControl>
                                            </FormItem>
                                        )}
                                    />
                                </div>
                            )}

                            <div className="bg-blue-50/70 border border-blue-100 p-6 rounded-xl space-y-2.5">
                                <h5 className="text-xs font-bold text-blue-700 uppercase tracking-widest">Tips:</h5>
                                <p className="text-xs text-blue-800 leading-relaxed italic">
                                    A privacy policy (also referred to as a privacy notice) is a statement or legal document that describes how a company, website, or app collects, uses, maintains, and shares information collected from its users to have a written privacy policy posted on the website.
                                </p>
                            </div>
                        </div>

                        {/* Navigation Buttons */}
                        <div className="flex items-center justify-between pt-8 border-t">
                            <Button type="button" variant="outline" className="border-slate-200 text-slate-600 hover:bg-slate-50 min-w-[100px]">
                                ← Back
                            </Button>
                            <div className="flex items-center gap-3">
                                <Button type="button" variant="ghost" className="text-slate-600 hover:text-slate-900 px-6">
                                    Save
                                </Button>
                                <Button type="submit" disabled={isLoading} className="bg-slate-900 hover:bg-slate-800 text-white min-w-[100px]">
                                    {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Next →"}
                                </Button>
                            </div>
                        </div>
                    </div>
                </form>
            </Form>
        </div>
    );
}
