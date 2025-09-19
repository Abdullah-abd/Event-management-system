// pages/_app.js
import Navbar from "@/components/Navbar/Navbar";
import { AuthProvider } from "@/context/AuthContext"; // ✅ import the provider, not the context
import "../styles/globals.css";

export default function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Navbar />
      <Component {...pageProps} />
    </AuthProvider>
  );
}
