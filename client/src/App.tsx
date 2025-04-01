function App() {
  const homePage = (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-4xl">Good Morning</h1>
    </div>
  );
  return <main className="h-screen container mx-auto">{homePage}</main>;
}

export default App;
