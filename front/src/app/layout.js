import { Inter } from "next/font/google";
import "./globals.css";
import Footer from "./components/Footer";
import Header from "./components/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "DI-WEIR",
  description: "A set of regulated algorithms for data operations.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
          <Header />
          <div style={{ minHeight: "90vh" }}>{children}</div>
          <Footer />
      </body>
    </html>
  );
}
