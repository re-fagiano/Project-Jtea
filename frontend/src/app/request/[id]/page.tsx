"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";

import ProtectedRoute from "@/components/auth/ProtectedRoute";
import AppHeader from "@/components/AppHeader";
import Card from "@/components/Card";
import { api, RichiestaDetail } from "@/lib/api";

export default function RequestDetailPage() {
    const params = useParams();
    const [richiesta, setRichiesta] = useState<RichiestaDetail | null>(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    const loadRequest = useCallback(async () => {
        const id = params.id as string;
        if (!id) {
            return;
        }

        setLoading(true);
        setError("");

        try {
            const data = await api.get<RichiestaDetail>(`/api/richieste/${id}`);
            setRichiesta(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Impossibile caricare, riprova.");
        } finally {
            setLoading(false);
        }
    }, [params.id]);

    useEffect(() => {
        loadRequest();
    }, [loadRequest]);

    return (
        <ProtectedRoute>
            <div className="min-h-screen bg-gray-950 text-gray-100">
                <AppHeader
                    title="Dettaglio richiesta"
                    subtitle="Stato, cliente e dettagli principali"
                />

                <main className="px-6 py-8 space-y-6">
                    {error && (
                        <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm space-y-3">
                            <p>{error}</p>
                            <button type="button" className="btn btn-outline" onClick={loadRequest}>
                                Riprova
                            </button>
                        </div>
                    )}

                    {loading ? (
                        <div className="text-gray-400">Caricamento richiesta...</div>
                    ) : !richiesta ? (
                        <div className="text-gray-400">Nessuna richiesta trovata.</div>
                    ) : (
                        <Card title={richiesta.titolo}>
                            <div className="space-y-3 text-sm text-gray-300">
                                <p>
                                    <span className="text-gray-400">Stato:</span> {richiesta.stato}
                                </p>
                                <p>
                                    <span className="text-gray-400">Cliente:</span> {richiesta.cliente.nome} ({richiesta.cliente.email})
                                </p>
                                <p>
                                    <span className="text-gray-400">Creato da:</span> {richiesta.utente.email}
                                </p>
                                {richiesta.descrizione && (
                                    <p>
                                        <span className="text-gray-400">Descrizione:</span> {richiesta.descrizione}
                                    </p>
                                )}
                            </div>
                        </Card>
                    )}
                </main>
            </div>
        </ProtectedRoute>
    );
}
