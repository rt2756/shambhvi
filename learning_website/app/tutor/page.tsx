import { TutorChat } from "@/components/TutorChat";

export default function TutorPage() {
  return (
    <div className="space-y-4">
      <header>
        <h1 className="text-3xl font-bold text-slate-900">AI Tutor</h1>
        <p className="mt-2 text-slate-600">
          Stuck on something? Type your question and I'll help you think it
          through.
        </p>
      </header>
      <TutorChat variant="page" />
    </div>
  );
}
