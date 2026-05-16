"use client";

import { useEffect } from "react";
import { recordChapterView } from "@/lib/progress/events";

// Records a chapter/foundation view after the reader stays >=30s,
// so a quick bounce does not count as study activity.
export function ViewTracker({ slug }: { slug: string }) {
  useEffect(() => {
    const timer = setTimeout(() => recordChapterView(slug), 30_000);
    return () => clearTimeout(timer);
  }, [slug]);

  return null;
}
