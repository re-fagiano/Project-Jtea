import Link from "next/link";

export default function Home() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 text-gray-100">
            <nav className="flex items-center justify-between px-6 py-6">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
                        <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                        </svg>
                    </div>
                    <span className="text-xl font-bold gradient-text">Project Jtea</span>
                </div>
                <Link href="/login" className="btn btn-primary">Accedi</Link>
            </nav>

            <main className="max-w-5xl mx-auto px-6 py-20 text-center">
                <h1 className="text-4xl md:text-5xl font-bold mb-6">
                    Gestisci ticket e clienti in un unico spazio
                </h1>
                <p className="text-lg text-gray-400 mb-10">
                    Dashboard semplice, flussi di lavoro essenziali e integrazione rapida con Railway.
                </p>
                <div className="flex flex-wrap justify-center gap-4">
                    <Link href="/login" className="btn btn-primary px-8 py-3 text-lg">
                        Vai al login
                    </Link>
                    <Link href="/dashboard" className="btn btn-outline px-8 py-3 text-lg">
                        Vai alla dashboard
                    </Link>
                </div>
            </main>

            <section className="max-w-5xl mx-auto px-6 pb-16 grid gap-6 md:grid-cols-3">
                {[
                    {
                        title: "Ticket rapidi",
                        desc: "Apri nuove richieste e monitora lo stato di avanzamento.",
                    },
                    {
                        title: "Clienti organizzati",
                        desc: "Gestisci clienti e contatti essenziali in pochi click.",
                    },
                    {
                        title: "Deploy semplice",
                        desc: "Configurazione pronta per Railway con Nixpacks.",
                    },
                ].map((item) => (
                    <div key={item.title} className="card glass p-6">
                        <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
                        <p className="text-gray-400">{item.desc}</p>
                    </div>
                ))}
            </section>
        </div>
    );
}
