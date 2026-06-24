import Navbar from "../components/layout/Navbar";

export default function Home() {
  return (
    <>
      <Navbar />

      <main className="mx-auto max-w-7xl p-6">
        <div className="grid grid-cols-12 gap-6">
          <section className="col-span-12 lg:col-span-8">
            <div
              className="
              min-h-162.5
              rounded-3xl
              border
              border-slate-800
              bg-slate-900/50
              backdrop-blur-xl
            "
            >
              <div className="border-b border-slate-800 p-6">
                <h2 className="text-xl font-semibold">
                  Analysis Workspace
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  Submit content for spam and emotion analysis.
                </p>
              </div>

              <div className="flex h-125 items-center justify-center">
                <div className="text-center">
                  <h3 className="text-lg font-medium">
                    Ready for Analysis
                  </h3>

                  <p className="mt-2 text-slate-400">
                    Enter a message below to begin.
                  </p>
                </div>
              </div>

              <div className="border-t border-slate-800 p-4">
                <div className="flex gap-3">
                  <select
                    className="
                    rounded-xl
                    border
                    border-slate-700
                    bg-slate-900
                    px-4
                    py-3
                    outline-none
                  "
                  >
                    <option>Spam Detection</option>
                    <option>Emotion Detection</option>
                  </select>

                  <input
                    type="text"
                    placeholder="Type your message..."
                    className="
                    flex-1
                    rounded-xl
                    border
                    border-slate-700
                    bg-slate-900
                    px-4
                    py-3
                    outline-none
                    focus:border-violet-500
                  "
                  />

                  <button
                    className="
                    rounded-xl
                    bg-violet-600
                    px-6
                    py-3
                    font-medium
                    transition
                    hover:bg-violet-500
                  "
                  >
                    Analyze
                  </button>
                </div>
              </div>
            </div>
          </section>

          <aside className="col-span-12 lg:col-span-4">
            <div
              className="
              rounded-3xl
              border
              border-slate-800
              bg-slate-900/50
              p-6
              backdrop-blur-xl
            "
            >
              <h2 className="mb-4 text-xl font-semibold">
                History
              </h2>

              <div className="rounded-2xl bg-slate-800/50 p-4">
                <p className="text-sm text-slate-400">
                  Login or Signup to view analysis history.
                </p>
              </div>
            </div>
          </aside>
        </div>
      </main>
    </>
  );
}