"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { login } from "@/lib/api";

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const data = await login(email, password);
            localStorage.setItem("token", data.access_token);
            router.push("/dashboard");
        } catch (err) {
            setError(err instanceof Error ? err.message : "Errore di connessione");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 px-4">
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute top-1/4 -left-20 w-72 h-72 bg-indigo-500/20 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 -right-20 w-72 h-72 bg-violet-500/15 rounded-full blur-3xl" />
            </div>

            <div className="relative w-full max-w-md">
                <div className="text-center mb-8">
                    <Link href="/" className="inline-flex items-center gap-3">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
                            <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                        </div>
                        <span className="text-2xl font-bold gradient-text">Project Jtea</span>
                    </Link>
                </div>

                <div className="card glass">
                    <h1 className="text-2xl font-bold text-center mb-2">Accedi</h1>
                    <p className="text-gray-400 text-center mb-8">Inserisci le credenziali per continuare</p>

                    {error && (
                        <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="input"
                                placeholder="nome@esempio.com"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="input"
                                placeholder="••••••••"
                                required
                            />
                        </div>

                        <button type="submit" disabled={loading} className="btn btn-primary w-full py-3 text-lg">
                            {loading ? "Accesso in corso..." : "Accedi"}
                        </button>
                    </form>

                    <p className="text-center text-gray-400 mt-6">
                        Non hai un account? <span className="text-indigo-400">Richiedi l'accesso</span>
                    </p>
                </div>
            </div>
        </div>
    );
}
