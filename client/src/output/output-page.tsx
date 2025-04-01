import { CopyIcon } from "lucide-react";
import React from "react";
import ReactMarkdown from "react-markdown";
const wsUrl = import.meta.env.VITE_WS_URL;

const markdownText = `
# Summary
The webpage content is about the Apple iPhone, its features, and purchasing options. The objective is to click on the top search result, but since this is a text-based analysis, we will extract relevant information from the webpage content instead.

## Introduction to iPhone
The iPhone is designed to be loved, with powerful possibilities and groundbreaking privacy protections. **Apple Intelligence** is a personal intelligence system that helps users write, express themselves, and get things done effortlessly.

## Key Features
- **Cutting-Edge Cameras**: Automatically capture phenomenal photos with great detail and color.
- **Chip and Battery Life**: Fast and long-lasting, with up to 33 hours of video playback on iPhone 16 Pro Max.
- **Innovation**: Beautiful and durable design, with a focus on accessibility and environmental sustainability.

## Purchasing Options
- **Get iPhone 16 from just ₹6325.00/mo.** for up to 12 mo. with No Cost EMI and instant cashback.
- **Apple Trade In**: Get instant trade-in credit for your new device, with options to trade in iPhone, Mac, or other devices.
- **Flexible Payment Options**: Choose from various payment methods, including credit/debit cards, RuPay, UPI, and Net Banking.

## Environmental Sustainability
- **Recycle, Reuse, Repeat**: Apple's disassembly robots recover crucial materials from recycled iPhone models.
- **95% Recycled Lithium**: Apple's latest models contain 95% recycled lithium in the battery cathode.
- **100% Fibre-Based Packaging**: iPhone packaging is now 100% fibre-based, with no plastic wrap.

## Privacy and Security
- **Groundbreaking Privacy Protections**: Apple Intelligence is integrated into the iPhone through on-device processing.
- **Private Browsing**: Safari locks browsing windows when not in use and blocks known trackers.
- **End-to-End Encryption**: iMessage uses end-to-end encryption between devices.

## Conclusion
The Apple iPhone offers a range of features, from cutting-edge cameras to innovative design and environmental sustainability. With various purchasing options and a focus on privacy and security, the iPhone is a great choice for those looking for a powerful and secure smartphone.`;

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
