"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import AppHeader from "@/components/AppHeader";
import Card from "@/components/Card";
import { api, Cliente } from "@/lib/api";

export default function NewRequestPage() {
    const router = useRouter();
    const [clienti, setClienti] = useState<Cliente[]>([]);
    const [clienteId, setClienteId] = useState("");
    const [titolo, setTitolo] = useState("");
    const [descrizione, setDescrizione] = useState("");
    const [stato, setStato] = useState("aperta");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            router.push("/login");
            return;
        }

        api.get<Cliente[]>("/api/clienti")
            .then(setClienti)
            .catch((err) => {
                setError(err instanceof Error ? err.message : "Errore caricamento clienti");
            });
    }, [router]);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError("");
        setLoading(true);

        try {
            const richiesta = await api.post<{ id: string }>("/api/richieste", {
                titolo,
                descrizione,
                stato,
                cliente_id: clienteId,
            });
            router.push(`/request/${richiesta.id}`);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Errore creazione richiesta");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100">
            <AppHeader title="Nuova richiesta" subtitle="Crea un ticket per un cliente" />

            <main className="px-6 py-8">
                {error && (
                    <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                        {error}
                    </div>
                )}

                <Card title="Dati richiesta" className="max-w-xl">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Cliente</label>
                            <select
                                className="input"
                                value={clienteId}
                                onChange={(event) => setClienteId(event.target.value)}
                                required
                            >
                                <option value="">Seleziona un cliente</option>
                                {clienti.map((cliente) => (
                                    <option key={cliente.id} value={cliente.id}>
                                        {cliente.nome} ({cliente.email})
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Titolo</label>
                            <input
                                className="input"
                                value={titolo}
                                onChange={(event) => setTitolo(event.target.value)}
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Descrizione</label>
                            <textarea
                                className="input min-h-[120px]"
                                value={descrizione}
                                onChange={(event) => setDescrizione(event.target.value)}
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-300 mb-2">Stato</label>
                            <input
                                className="input"
                                value={stato}
                                onChange={(event) => setStato(event.target.value)}
                            />
                        </div>

                        <button type="submit" className="btn btn-primary w-full" disabled={loading}>
                            {loading ? "Creazione in corso..." : "Crea richiesta"}
                        </button>
                    </form>
                </Card>
            </main>
        </div>
    );
}
