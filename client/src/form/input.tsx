import { cn } from "@/lib/utils";
import { Dispatch, SetStateAction } from "react";
import { ArrowUp } from "lucide-react";
const FormInput = ({
  handleSubmit,
  className,
  query,
  setQuery,
}: {
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  className?: string;
  query: string;
  setQuery: Dispatch<SetStateAction<string>>;
}) => {
  return (
    <form
      onSubmit={handleSubmit}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          handleSubmit(e);
        }
      }}
      className={cn(
        "rounded-lg w-full max-w-[900px] px-4 py-2 flex flex-col bg-neutral-50 border border-neutral-200",
        className
      )}
    >
      <textarea
        placeholder={"What do you want to do?"}
        className="w-full outline-none resize-none overflow-y-hidden min-h-[4rem] font-medium"
        style={{ height: "auto" }}
        onInput={(e) => {
          const target = e.target as HTMLTextAreaElement;
          target.style.height = "0px";
          target.style.height = `${target.scrollHeight}px`;
        }}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <main className="h-12 flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs"></div>
        <div className="flex items-center gap-2">
          <button
            type="submit"
            className={cn(
              "w-9 h-9 rounded-full flex items-center justify-center",
              "transition-colors cursor-pointer",
              "bg-neutral-600 hover:bg-neutral-700"
            )}
          >
            <ArrowUp className="text-white" />
          </button>
        </div>
      </main>
    </form>
  );
};

export default FormInput;
