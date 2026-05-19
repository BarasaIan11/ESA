import axios from "axios";
import type { AskRequest, AskResponse, TokenResponse } from "../types";

// Locally:     reads from frontend/.env
// On Vercel:   reads from Vercel env dashboard
const API_BASE = import.meta.env.VITE_API_BASE_URL as string;

if (!API_BASE) {
  console.error(
    "[ESA] VITE_API_BASE_URL is not set. " +
      "Add it to frontend/.env for local dev, or to Vercel environment variables for production.",
  );
}

// Token Cache
// Cache the token in memory for this session
let _token: string | null = null;

async function getToken(): Promise<string> {
  if (_token) return _token;
  const resp = await axios.post<TokenResponse>(`${API_BASE}/auth/token`, {
    api_key: import.meta.env.VITE_API_KEY ?? "secret-key", // Replace with a login flow later
  });
  _token = resp.data.access_token;
  return _token;
}

// API Calls
export async function askQuestion(request: AskRequest): Promise<AskResponse> {
  const token = await getToken();
  const resp = await axios.post<AskResponse>(`${API_BASE}/chat/ask`, request, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return resp.data;
}
