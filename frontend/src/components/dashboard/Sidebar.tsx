"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/request/new", label: "Nuova richiesta" },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="hidden md:flex md:w-64 border-r border-gray-800 bg-gray-900/60 p-4 flex-col gap-3">
            <div className="px-2 py-3 text-lg font-semibold">Project Jtea</div>
            <nav className="space-y-2">
                {links.map((link) => {
                    const isActive = pathname === link.href;
                    return (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={`block rounded-md px-3 py-2 text-sm transition ${
                                isActive ? "bg-indigo-500/20 text-indigo-300" : "text-gray-300 hover:bg-gray-800"
                            }`}
                        >
                            {link.label}
                        </Link>
                    );
                })}
            </nav>
        </aside>
    );
}
