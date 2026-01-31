"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import AppHeader from "@/components/AppHeader";
import Card from "@/components/Card";
import { api, RichiestaDetail } from "@/lib/api";

export default function RequestDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [richiesta, setRichiesta] = useState<RichiestaDetail | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            router.push("/login");
            return;
        }

        const id = params.id as string;
        api.get<RichiestaDetail>(`/api/richieste/${id}`)
            .then(setRichiesta)
            .catch((err) => {
                setError(err instanceof Error ? err.message : "Errore caricamento");
            });
    }, [params.id, router]);

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100">
            <AppHeader
                title="Dettaglio richiesta"
                subtitle="Stato, cliente e dettagli principali"
            />

            <main className="px-6 py-8 space-y-6">
                {error && (
                    <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                        {error}
                    </div>
                )}

                {!richiesta ? (
                    <div className="text-gray-400">Caricamento richiesta...</div>
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
    );
}
