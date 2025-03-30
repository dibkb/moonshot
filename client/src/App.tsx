import { useState } from "react";

import { useEffect, useRef } from "react";

function App() {
  const eventSourceRef = useRef<EventSource | null>(null);
  const [data, setData] = useState<string[]>([]);
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);
  const handleSubmitSemantic = () => {
    eventSourceRef.current = new EventSource(
      `${"http://localhost:8090"}/visual-elements`
    );

    eventSourceRef.current.onmessage = (event) => {
      console.log(event.data);
      setData((prev) => [...prev, event.data]);
    };

    eventSourceRef.current.onerror = () => {
      eventSourceRef.current?.close();
      eventSourceRef.current = null;
    };
  };
  return (
    <>
      <button onClick={handleSubmitSemantic}>submit</button>

      {data.map((item) => (
        <div key={item}>{item}</div>
      ))}
    </>
  );
}

export default App;
