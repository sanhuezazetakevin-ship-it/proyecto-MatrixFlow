
import React from "react";
import { X } from "lucide-react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-white dark:bg-brand-darker w-full max-w-md rounded-2xl shadow-2xl border border-slate-200 dark:border-brand-dark overflow-hidden animate-slide-up">
        <div className="flex items-center justify-between p-4 border-b border-slate-200 dark:border-brand-dark bg-slate-50 dark:bg-brand-darkest">
          <h2 className="text-sm font-bold text-slate-800 dark:text-white">{title}</h2>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-200 dark:hover:bg-brand-dark text-slate-500 transition-colors">
            <X size={18} />
          </button>
        </div>
        <div className="p-5">
          {children}
        </div>
      </div>
    </div>
  );
};
