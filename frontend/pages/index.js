"use-client";
// pages/index.js
import Navbar from "../components/Navbar/Navbar";

export default function Home() {
  return (
    <div>
      <Navbar />
      <main className="p-6">
        <h1 className="text-2xl font-bold">Welcome to Event Manager</h1>
        <p className="mt-2 text-gray-600">
          Browse and manage events with ease.
        </p>
      </main>
    </div>
  );
}
