import { useState } from "react";
import { ArrowRight, RefreshCw, X, ChevronLeft, ChevronRight } from "lucide-react";
import Navbar from "../components/layout/Navbar";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { isAuthenticated } = useAuth();

  const [input, setInput]     = useState("");
  const [query, setQuery]     = useState("");
  const [reply, setReply]     = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone]       = useState(false);
  const [model, setModel]     = useState("spam");

  async function handleSubmit() {
    if (!input.trim() || loading) return;
    setQuery(input.trim());
    setInput("");
    setReply("");
    setDone(false);
    setLoading(true);
    // TODO: replace with real FastAPI call
    await new Promise((r) => setTimeout(r, 1200));
    setReply("Analysis complete — content appears to be non-spam with a neutral sentiment.");
    setLoading(false);
    setDone(true);
  }

  function handleClear() {
    setQuery("");
    setReply("");
    setDone(false);
    setInput("");
  }

  const hasContent = query || loading || reply;

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-7xl p-6">
        <div className="grid grid-cols-12 gap-6">

          <section className="col-span-12 lg:col-span-8">
            <div className="flex min-h-[650px] flex-col rounded-3xl border border-slate-800 bg-slate-900/50 backdrop-blur-xl">

              <div className="flex-1 space-y-4 overflow-y-auto p-6">
                {!hasContent ? (
                  <div className="flex min-h-[480px] items-center justify-center">
                    <div className="text-center">
                      <div className="mx-auto mb-4 grid h-14 w-14 place-items-center rounded-2xl bg-violet-600/20 text-violet-400">
                        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-semibold">Ready for Analysis</h3>
                      <p className="mt-1 text-sm text-slate-400">
                        Enter a message below to begin.
                      </p>
                    </div>
                  </div>
                ) : (
                  <>
                    {query && (
                      <div className="rounded-2xl border border-slate-700 bg-slate-800/60 p-4">
                        <p className="mb-1.5 text-[10px] font-bold uppercase tracking-widest text-slate-500">
                          Your Query
                        </p>
                        <p className="text-sm leading-relaxed text-slate-200">{query}</p>
                      </div>
                    )}

                    {loading ? (
                      <div className="rounded-2xl border border-violet-800/40 bg-violet-950/30 p-4">
                        <p className="mb-3 text-[10px] font-bold uppercase tracking-widest text-violet-400/70">
                          Analyzing
                        </p>
                        <div className="flex gap-1.5">
                          {[0, 150, 300].map((d) => (
                            <span
                              key={d}
                              className="h-2 w-2 animate-bounce rounded-full bg-violet-400"
                              style={{ animationDelay: `${d}ms` }}
                            />
                          ))}
                        </div>
                      </div>
                    ) : reply ? (
                      <div className="rounded-2xl border border-slate-700 bg-slate-800/30 p-4">
                        <p className="mb-1.5 text-[10px] font-bold uppercase tracking-widest text-slate-500">
                          Result
                        </p>
                        <p className="text-sm leading-relaxed text-slate-200">{reply}</p>
                      </div>
                    ) : null}
                  </>
                )}
              </div>

              <div className="border-t border-slate-800 p-4">
                {done ? (
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-slate-500">Analysis complete.</p>
                    <div className="flex gap-2">
                      <button
                        onClick={handleClear}
                        className="flex items-center gap-1.5 rounded-xl border border-slate-700 px-4 py-2 text-sm transition hover:border-slate-500"
                      >
                        <X size={13} />
                        Clear
                      </button>
                      <button
                        onClick={handleClear}
                        className="flex items-center gap-1.5 rounded-xl bg-violet-600 px-4 py-2 text-sm font-medium transition hover:bg-violet-500"
                      >
                        <RefreshCw size={13} />
                        New Analysis
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex gap-2">
                    <div className="relative shrink-0">
                      <select
                        value={model}
                        onChange={(e) => {
                          if (!isAuthenticated) return;
                          setModel(e.target.value);
                        }}
                        title={!isAuthenticated ? "Login to switch models" : ""}
                        className="h-full cursor-pointer appearance-none rounded-xl border border-slate-700 bg-slate-900 px-3 py-3 pr-6 text-sm outline-none transition focus:border-violet-500"
                      >
                        <option value="spam">Spam</option>
                        <option value="emotion" disabled={!isAuthenticated}>
                          {isAuthenticated ? "Emotion" : "Emotion (login)"}
                        </option>
                      </select>
                      {!isAuthenticated && (
                        <span className="pointer-events-none absolute -right-1 -top-1 flex h-3 w-3">
                          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-violet-400 opacity-60" />
                          <span className="relative inline-flex h-3 w-3 rounded-full bg-violet-500" />
                        </span>
                      )}
                    </div>

                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
                      placeholder="Type your message…"
                      className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm outline-none transition placeholder:text-slate-600 focus:border-violet-500"
                    />

                    <button
                      onClick={handleSubmit}
                      disabled={!input.trim() || loading}
                      className="grid place-items-center rounded-xl bg-violet-600 px-4 py-3 transition hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      <ArrowRight size={18} />
                    </button>
                  </div>
                )}
              </div>
            </div>
          </section>
          <aside className="col-span-12 lg:col-span-4">
            <div className="flex min-h-[650px] flex-col rounded-3xl border border-slate-800 bg-slate-900/50 backdrop-blur-xl">
              <div className="border-b border-slate-800 px-6 py-4">
                <h2 className="text-xl font-semibold">History</h2>
              </div>

              <div className="flex-1 overflow-y-auto p-4">
                {!isAuthenticated ? (
                  <div className="flex flex-col items-center gap-3 rounded-2xl bg-slate-800/50 p-6 text-center">
                    <p className="text-sm text-slate-400">
                      Sign in to save and view your analysis history.
                    </p>
                    <button className="w-full rounded-xl bg-violet-600 py-2.5 text-sm font-medium transition hover:bg-violet-500">
                      Login
                    </button>
                    <button className="w-full rounded-xl border border-slate-700 py-2.5 text-sm transition hover:border-violet-500">
                      Sign Up
                    </button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {/* TODO: replace with real paginated API data */}
                    {Array.from({ length: 6 }, (_, i) => (
                      <div
                        key={i}
                        className="cursor-pointer rounded-xl border border-slate-700/40 bg-slate-800/30 p-3 transition hover:border-violet-500/50"
                      >
                        <p className="truncate text-sm text-slate-300">
                          Sample analysis query {i + 1}
                        </p>
                        <div className="mt-1 flex items-center justify-between">
                          <span className="rounded-md bg-slate-700/60 px-1.5 py-0.5 text-[10px] text-slate-400">
                            Spam
                          </span>
                          <span className="text-xs text-slate-600">2 min ago</span>
                        </div>
                      </div>
                    ))}

                    <div className="flex items-center justify-center gap-2 pt-2">
                      <button className="grid h-8 w-8 place-items-center rounded-lg border border-slate-700 text-slate-400 transition hover:border-violet-500 hover:text-violet-400">
                        <ChevronLeft size={14} />
                      </button>
                      <span className="text-xs text-slate-500">Page 1 of 4</span>
                      <button className="grid h-8 w-8 place-items-center rounded-lg border border-slate-700 text-slate-400 transition hover:border-violet-500 hover:text-violet-400">
                        <ChevronRight size={14} />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </aside>

        </div>
      </main>
    </>
  );
}