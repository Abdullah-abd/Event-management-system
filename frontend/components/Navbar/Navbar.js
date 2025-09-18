"use client";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    router.push("/login"); // redirect to login page
  };

  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between items-center">
      {/* Logo */}
      <div className="text-xl font-bold">EVS</div>

      {/* Links */}
      <div className="flex space-x-4 items-center">
        {!isLoggedIn ? (
          <>
            <Link
              href="/login"
              className="bg-white text-blue-600 px-3 py-1 rounded-lg font-medium hover:bg-gray-100"
            >
              Login
            </Link>

            <Link
              href="/signup"
              className="bg-white text-blue-600 px-3 py-1 rounded-lg font-medium hover:bg-gray-100"
            >
              Signup
            </Link>
          </>
        ) : (
          <button
            onClick={handleLogout}
            className="bg-white text-blue-600 px-3 py-1 rounded-lg font-medium hover:bg-gray-100"
          >
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}
