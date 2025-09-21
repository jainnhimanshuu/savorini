/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  experimental: {
    serverComponentsExternalPackages: ["@happyhour/types"],
  },
  transpilePackages: ["@happyhour/types", "@happyhour/ui"],
  images: {
    domains: ["localhost", "example.com"], // Add your image domains
  },
  env: {
    NEXT_PUBLIC_API_URL:
      process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
};

module.exports = nextConfig;
