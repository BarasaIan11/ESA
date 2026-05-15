import axios from 'axios';
import type { AskRequest, AskResponse, TokenResponse } from '../types';

const API_BASE = 'http://127.0.0.1:8000';

// Cache the token in memory for this session
let _token: string | null = null;

async function getToken(): Promise<string> {
  if (_token) return _token;
  const resp = await axios.post<TokenResponse>(`${API_BASE}/auth/token`, {
    api_key: 'secret-key', // Demo key — this will be replaced by a login flow later
  });
  _token = resp.data.access_token;
  return _token;
}

export async function askQuestion(request: AskRequest): Promise<AskResponse> {
  const token = await getToken();
  const resp = await axios.post<AskResponse>(`${API_BASE}/chat/ask`, request, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return resp.data;
}
