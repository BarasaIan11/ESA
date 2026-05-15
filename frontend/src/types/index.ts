export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: string[];
  timestamp: Date;
}

export interface AskRequest {
  question: string;
  session_id?: string;
}

export interface AskResponse {
  answer: string;
  session_id: string;
  sources: string[];
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
