"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

import AppHeader from "@/components/AppHeader";
import Card from "@/components/Card";
import { api, Richiesta, User } from "@/lib/api";

export default function DashboardPage() {
    const [user, setUser] = useState<User | null>(null);
    const [richieste, setRichieste] = useState<Richiesta[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadData = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const [userData, richiesteData] = await Promise.all([
                api.get<User>("/users/me"),
                api.get<Richiesta[]>("/api/richieste"),
            ]);

            setUser(userData);
            setRichieste(richiesteData);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Impossibile caricare, riprova.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadData();
    }, [loadData]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <>
            <AppHeader
                title="Dashboard"
                subtitle={user ? `Bentornato, ${user.email}` : undefined}
                action={
                    <Link href="/request/new" className="btn btn-primary">
                        Nuova richiesta
                    </Link>
                }
            />

            <main className="px-6 py-8 space-y-6">
                {error && (
                    <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm space-y-3">
                        <p>{error || "Impossibile caricare, riprova."}</p>
                        <button type="button" className="btn btn-outline" onClick={loadData}>
                            Riprova
                        </button>
                    </div>
                )}

                <Card title="Richieste recenti">
                    {richieste.length === 0 ? (
                        <p className="text-gray-400">Nessuna richiesta trovata.</p>
                    ) : (
                        <div className="space-y-4">
                            {richieste.map((richiesta) => (
                                <Link
                                    key={richiesta.id}
                                    href={`/request/${richiesta.id}`}
                                    className="block rounded-lg border border-gray-800 p-4 hover:border-indigo-500/40 transition"
                                >
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <h3 className="font-semibold">{richiesta.titolo}</h3>
                                            <p className="text-sm text-gray-400">
                                                Stato: {richiesta.stato}
                                            </p>
                                        </div>
                                        <span className="text-xs text-gray-500">
                                            {new Date(richiesta.created_at).toLocaleDateString("it-IT")}
                                        </span>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    )}
                </Card>
            </main>
        </>
    );
}
