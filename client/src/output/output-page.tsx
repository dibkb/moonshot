import { CopyIcon } from "lucide-react";
import React from "react";
import ReactMarkdown from "react-markdown";
const wsUrl = import.meta.env.VITE_WS_URL;

const OutputPage = ({ taskId }: { taskId: string }) => {
  const [messages, setMessages] = React.useState<string[]>([]);
  const [markdown, setMarkdown] = React.useState<string>("");
  React.useEffect(() => {
    // Create WebSocket connection
    const ws = new WebSocket(`${wsUrl}/${taskId}`);

    // Handle incoming messages
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "llm") {
        setMessages((prev) => [...prev, "🤖 : " + data.message]);
      } else if (data.type === "information") {
        setMarkdown(data.message);
      }
    };

    // Handle connection errors
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    // Cleanup on component unmount
    return () => {
      ws.close();
    };
  }, [taskId]);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(markdown);
  };

  return (
    <div className="py-4 px-4 overflow-x-scroll">
      <main className="h-full w-full rounded-lg p-4 overflow-x-scroll">
        {messages.map((message, index) => (
          <div key={index} className="mb-1 text-sm text-neutral-500">
            {message}
          </div>
        ))}
        {markdown && (
          <section className="bg-neutral-50 rounded-lg relative">
            <div className="absolute top-0 w-full h-[35px] px-4 py-1 flex items-center justify-between bg-neutral-200 rounded-t-lg text-sm">
              <p className="">{"text"}</p>
              <button
                onClick={copyToClipboard}
                className="flex items-center gap-1 text-xs cursor-pointer hover:bg-neutral-300 px-2 py-1 rounded-md"
              >
                Copy
                <CopyIcon className="w-4 h-4" />
              </button>
            </div>
            <main className="pt-[35px] px-4 pb-4">
              <ReactMarkdown>{markdown}</ReactMarkdown>
            </main>
          </section>
        )}
      </main>
    </div>
  );
};

export default OutputPage;
