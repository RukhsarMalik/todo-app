'use client';

import { getToken } from './auth';
import { API_CONFIG } from './constants';

interface SendMessageRequest {
  message: string;
  conversation_id?: string;
}

interface SendMessageResponse {
  response: string;
  conversation_id: string;
  message_id: string;
  actions_taken: Array<{
    tool: string;
    result: string;
    task_id?: string;
  }>;
}

/**
 * Send a message to the chat endpoint
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string
): Promise<SendMessageResponse> {
  const token = getToken();
  const response = await fetch(`${API_CONFIG.baseUrl}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Chat API request failed: ${response.status} ${response.statusText}. ${errorText}`);
  }

  return response.json();
}

/**
 * Get conversation history
 */
export async function getConversationHistory(
  userId: string,
  conversationId: string
): Promise<any[]> {
  const token = getToken();
  const response = await fetch(`${API_CONFIG.baseUrl}/api/${userId}/conversations/${conversationId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error(`Get conversation history failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}