import { useEffect, useRef, useState } from "react";

import ChatInput from "./ChatInput";
import Message from "./Message";
import { sendMessage } from "../services/api";


function ChatWindow({
  conversationId,
  setConversationId,
  messages,
  setMessages,
}) {

  const [isLoading, setIsLoading] =
    useState(false);

  const messagesEndRef =
    useRef(null);


  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages, isLoading]);


  async function handleSendMessage(
    query,
  ) {

    if (!query.trim() || isLoading) {
      return;
    }


    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: query.trim(),
    };


    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);


    setIsLoading(true);


    try {

      const result =
        await sendMessage(
          query,
          conversationId,
        );


      if (
        !conversationId &&
        result.conversation_id
      ) {

        setConversationId(
          result.conversation_id,
        );

      }


      const assistantMessage = {
        id: result.request_id ||
          crypto.randomUUID(),

        role: "assistant",

        content:
          result.answer,

        sources:
          result.sources || [],

        grounded:
          result.grounded,

        cached:
          result.cached,

        metrics:
          result.metrics,
      };


      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);

    } catch (error) {

      const errorMessage = {
        id: crypto.randomUUID(),

        role: "assistant",

        content:
          `Error: ${error.message}`,

        isError: true,
      };


      setMessages((previous) => [
        ...previous,
        errorMessage,
      ]);

    } finally {

      setIsLoading(false);

    }

  }


  return (
    <div className="chat-window">

      <div className="chat-header">

        <div>

          <h1>
            AI Knowledge Assistant
          </h1>

          <p>
            Ask questions about your
            uploaded documents
          </p>

        </div>

        <div className="status-indicator">

          <span className="status-dot" />

          AI Online

        </div>

      </div>


      <div className="messages-container">

        {messages.length === 0 && (

          <div className="empty-chat">

            <div className="empty-icon">
              ✦
            </div>

            <h2>
              How can I help you?
            </h2>

            <p>
              Upload documents and ask
              questions about them.
            </p>

          </div>

        )}


        {messages.map((message) => (

          <Message
            key={message.id}
            message={message}
          />

        ))}


        {isLoading && (

          <div className="typing-message">

            <div className="typing-avatar">
              AI
            </div>

            <div className="typing-content">

              <span />

              <span />

              <span />

            </div>

          </div>

        )}


        <div ref={messagesEndRef} />

      </div>


      <ChatInput
        onSend={handleSendMessage}
        disabled={isLoading}
      />

    </div>
  );

}


export default ChatWindow;