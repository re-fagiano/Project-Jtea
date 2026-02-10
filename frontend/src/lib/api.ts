import { API_URL } from "@/lib/config";

interface FetchOptions extends RequestInit {
    requireAuth?: boolean;
}

type UnauthorizedHandler = () => void;
type TokenGetter = () => string | null;

let getToken: TokenGetter = () => (typeof window !== "undefined" ? localStorage.getItem("token") : null);
let onUnauthorized: UnauthorizedHandler = () => {};

export function setApiAuthHandlers(handlers: {
    getToken?: TokenGetter;
    onUnauthorized?: UnauthorizedHandler;
}) {
    if (handlers.getToken) {
        getToken = handlers.getToken;
    }
    if (handlers.onUnauthorized) {
        onUnauthorized = handlers.onUnauthorized;
    }
}

export async function apiFetch<T>(path: string, options: FetchOptions = {}): Promise<T> {
    const { requireAuth = true, headers: customHeaders, ...fetchOptions } = options;

    const headers = new Headers(customHeaders);
    if (!headers.has("Content-Type") && !(fetchOptions.body instanceof FormData)) {
        headers.set("Content-Type", "application/json");
    }

    if (requireAuth) {
        const token = getToken();
        if (!token) {
            onUnauthorized();
            throw new Error("Sessione non valida. Effettua di nuovo il login.");
        }
        headers.set("Authorization", `Bearer ${token}`);
    }

    const response = await fetch(`${API_URL}${path}`, {
        ...fetchOptions,
        headers,
    });

    if (response.status === 401) {
        onUnauthorized();
        throw new Error("Sessione scaduta. Effettua di nuovo il login.");
    }

    const isJson = response.headers.get("content-type")?.includes("application/json");
    const payload = isJson ? await response.json().catch(() => null) : null;

    if (!response.ok) {
        const detail = payload && typeof payload === "object" && "detail" in payload
            ? String(payload.detail)
            : null;
        throw new Error(detail || `Impossibile completare la richiesta (${response.status}).`);
    }

    return payload as T;
}

export async function login(email: string, password: string) {
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    return apiFetch<{ access_token: string }>("/login", {
        method: "POST",
        body: formData,
        requireAuth: false,
    });
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
