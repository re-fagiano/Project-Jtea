"use client";

import Link from "next/link";

import { useAuth } from "@/context/AuthContext";

interface AppHeaderProps {
    title: string;
    subtitle?: string;
    action?: React.ReactNode;
}

export default function AppHeader({ title, subtitle, action }: AppHeaderProps) {
    const { logout } = useAuth();

    return (
        <header className="flex flex-col gap-4 border-b border-gray-800 bg-gray-950/70 px-6 py-5 md:flex-row md:items-center md:justify-between">
            <div>
                <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
                        <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                    </div>
                    <div>
                        <h1 className="text-2xl font-semibold">{title}</h1>
                        {subtitle && <p className="text-sm text-gray-400">{subtitle}</p>}
                    </div>
                </div>
            </div>
            <div className="flex items-center gap-3">
                <Link href="/dashboard" className="btn btn-ghost">
                    Dashboard
                </Link>
                {action}
                <button type="button" className="btn btn-outline" onClick={logout}>
                    Logout
                </button>
            </div>
        </header>
    );
}
