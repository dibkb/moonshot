import { cn } from "./lib/utils";

import FormInput from "./form/input";
import { useState } from "react";
import OutputPage from "./output/output-page";
import axiosInstance from "./axios";
function App() {
  const [query, setQuery] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [taskId, setTaskId] = useState<string | null>("x");
  const submitQueryHandler = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStreaming(true);
    const response = await axiosInstance.post("/tasks", {
      query,
    });
    const data = response.data;
    if (data.task_id) {
      setStreaming(false);
      setTaskId(data.task_id);
    }
  };
  const renderPage = (homepage: boolean = false) => {
    return (
      <div
        className={cn(
          "flex flex-col items-center justify-center h-full",
          homepage && "col-span-2"
        )}
      >
        <div className="flex flex-col gap-5 items-center justify-center w-full">
          <h1 className="text-4xl">Good Morning</h1>
          <h3 className="text-3xl text-neutral-500">
            How can I help you today?
          </h3>
          <FormInput
            handleSubmit={submitQueryHandler}
            query={query}
            setQuery={setQuery}
            className="mt-9 w-full"
            streaming={streaming}
          />
        </div>
      </div>
    );
  };
  return (
    <main className="h-screen container mx-auto grid grid-cols-2 gap-3">
      {renderPage()}
      {taskId && <OutputPage taskId={taskId} />}
    </main>
  );
}

export default App;
