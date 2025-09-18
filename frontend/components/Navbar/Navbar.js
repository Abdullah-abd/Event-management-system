"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
      {/* Logo */}
      <div className="text-xl font-bold">EVS</div>

      {/* Links */}
      <div className="flex space-x-4 items-center">
        {/* Login */}
        <Link
          href="/login"
          className="bg-white text-blue-600 px-3 py-1 rounded-lg font-medium hover:bg-gray-100"
        >
          Login
        </Link>

        {/* Signup */}
        <Link
          href="/signup"
          className="bg-white text-blue-600 px-3 py-1 rounded-lg font-medium hover:bg-gray-100"
        >
          Signup
        </Link>
      </div>
    </nav>
  );
}
