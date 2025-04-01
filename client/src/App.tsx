import { cn } from "./lib/utils";

import FormInput from "./form/input";
import { useState } from "react";
import OutputPage from "./output/output-page";
function App() {
  const [query, setQuery] = useState("");
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
            handleSubmit={() => {}}
            query={query}
            setQuery={setQuery}
            className="mt-9 w-full"
          />
        </div>
      </div>
    );
  };
  return (
    <main className="h-screen container mx-auto grid grid-cols-2 gap-3">
      {renderPage()}
      <OutputPage />
    </main>
  );
}

export default App;
