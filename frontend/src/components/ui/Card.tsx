import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return (
    <div 
      className={`matrix-card rounded-2xl p-5 transition-all duration-300 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<{ title: string; subtitle?: string; action?: React.ReactNode }> = ({
  title, subtitle, action
}) => (
  <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-200 dark:border-brand-dark">
    <div>
      <h3 className="matrix-card-title font-extrabold text-lg tracking-tight">{title}</h3>
      {subtitle && <p className="matrix-card-subtitle text-xs font-semibold mt-0.5">{subtitle}</p>}
    </div>
    {action && <div>{action}</div>}
  </div>
);
