import type { Metadata } from "next";

import Providers from "@/app/providers";

import "./globals.css";

export const metadata: Metadata = {
    title: "Project Jtea",
    description: "Piattaforma MVP per la gestione ticket e clienti",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="it" className="dark">
            <body className="font-sans antialiased bg-gray-950 text-white min-h-screen">
                <Providers>{children}</Providers>
            </body>
        </html>
    );
}
