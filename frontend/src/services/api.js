const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";


async function request(
  endpoint,
  options = {},
) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      headers: {
        "Content-Type":
          "application/json",
        ...options.headers,
      },
      ...options,
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Something went wrong.",
    );
  }

  return data;
}


// ----------------------------------------
// CHAT
// ----------------------------------------

export async function sendMessage(
  query,
  conversationId = null,
) {
  return request(
    "/api/chat/",
    {
      method: "POST",
      body: JSON.stringify({
        query,
        conversation_id:
          conversationId,
      }),
    },
  );
}


// ----------------------------------------
// CONVERSATIONS
// ----------------------------------------

export async function createConversation() {
  return request(
    "/api/conversations/",
    {
      method: "POST",
      body: JSON.stringify({
        user_id: "default_user",
      }),
    },
  );
}


export async function getConversation(
  conversationId,
) {
  return request(
    `/api/conversations/${conversationId}`,
  );
}


export async function deleteConversation(
  conversationId,
) {
  return request(
    `/api/conversations/${conversationId}`,
    {
      method: "DELETE",
    },
  );
}


// ----------------------------------------
// DOCUMENTS
// ----------------------------------------

export async function uploadDocument(
  file,
) {
  const formData = new FormData();

  formData.append(
    "file",
    file,
  );

  const response = await fetch(
    `${API_BASE_URL}/api/documents/upload`,
    {
      method: "POST",
      body: formData,
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Failed to upload document.",
    );
  }

  return data;
}


// ----------------------------------------
// HEALTH
// ----------------------------------------

export async function checkHealth() {
  return request(
    "/api/health",
  );
}