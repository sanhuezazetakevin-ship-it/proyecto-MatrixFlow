import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'accent';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-200 active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-xs';
  
  const variants = {
    primary: 'bg-brand-teal text-white hover:bg-brand-dark focus:ring-brand-teal dark:bg-brand-teal dark:hover:bg-brand-mint dark:hover:text-brand-darkest',
    accent: 'bg-brand-mint text-brand-darkest hover:bg-brand-mintHover focus:ring-brand-mint font-bold',
    secondary: 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-brand-dark dark:text-slate-200 dark:hover:bg-brand-darker focus:ring-brand-teal',
    outline: 'border border-slate-300 dark:border-brand-dark bg-transparent text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-brand-darker focus:ring-brand-teal',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-5 py-2.5 text-base gap-2.5',
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
