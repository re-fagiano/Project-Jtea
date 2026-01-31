interface CardProps {
    title?: string;
    children: React.ReactNode;
    className?: string;
}

export default function Card({ title, children, className = "" }: CardProps) {
    return (
        <section className={`card glass p-6 ${className}`}>
            {title && <h2 className="text-lg font-semibold mb-4">{title}</h2>}
            {children}
        </section>
    );
}
