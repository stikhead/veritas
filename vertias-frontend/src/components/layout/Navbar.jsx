import { ShieldCheck } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated } = useAuth();

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-violet-600 p-2">
            <ShieldCheck size={20} />
          </div>

          <div>
            <h1 className="text-lg font-bold">Veritas</h1>
            <p className="text-xs text-slate-400">
              AI Content Analyzer
            </p>
          </div>
        </div>

        {!isAuthenticated ? (
          <div className="flex gap-3">
            <button
              className="
              rounded-xl
              border
              border-slate-700
              px-5
              py-2
              transition
              hover:border-violet-500
            "
            >
              Login
            </button>

            <button
              className="
              rounded-xl
              bg-violet-600
              px-5
              py-2
              font-medium
              transition
              hover:bg-violet-500
            "
            >
              Signup
            </button>
          </div>
        ) : (
          <div className="h-10 w-10 rounded-full bg-violet-600" />
        )}
      </div>
    </nav>
  );
}