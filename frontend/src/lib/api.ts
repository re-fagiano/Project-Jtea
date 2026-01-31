"""
API Client per comunicazione con backend FastAPI.
"""

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
    requireAuth?: boolean;
}

export async function apiFetch<T>(
    endpoint: string,
    options: FetchOptions = {}
): Promise<T> {
    const { requireAuth = true, ...fetchOptions } = options;

    const headers: HeadersInit = {
        "Content-Type": "application/json",
        ...fetchOptions.headers,
    };

    if (requireAuth) {
        const token = localStorage.getItem("token");
        if (!token) {
            throw new Error("Non autenticato");
        }
        (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...fetchOptions,
        headers,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Errore ${response.status}`);
    }

    return response.json();
}

export async function login(email: string, password: string) {
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Errore di autenticazione");
    }

    return response.json();
}

export const api = {
    get: <T>(endpoint: string, options?: FetchOptions) =>
        apiFetch<T>(endpoint, { ...options, method: "GET" }),

    post: <T>(endpoint: string, data?: unknown, options?: FetchOptions) =>
        apiFetch<T>(endpoint, {
            ...options,
            method: "POST",
            body: data ? JSON.stringify(data) : undefined,
        }),

    put: <T>(endpoint: string, data?: unknown, options?: FetchOptions) =>
        apiFetch<T>(endpoint, {
            ...options,
            method: "PUT",
            body: data ? JSON.stringify(data) : undefined,
        }),

    delete: <T>(endpoint: string, options?: FetchOptions) =>
        apiFetch<T>(endpoint, { ...options, method: "DELETE" }),
};

export interface User {
    id: string;
    email: string;
    ruolo: "admin" | "supervisore" | "tecnico" | "cliente";
}

export interface Cliente {
    id: string;
    nome: string;
    email: string;
}

export interface Richiesta {
    id: string;
    titolo: string;
    descrizione?: string;
    stato: string;
    cliente_id: string;
    utente_id: string;
    created_at: string;
}

export interface RichiestaDetail extends Richiesta {
    cliente: Cliente;
    utente: User;
}
