import { useState } from "react";

import DocumentPanel from "./DocumentPanel";

import {
  createConversation,
  deleteConversation,
  getConversation,
} from "../services/api";


function Sidebar({
  conversations,
  setConversations,
  conversationId,
  setConversationId,
  setMessages,
}) {

  const [isLoading, setIsLoading] =
    useState(false);


  async function handleNewConversation() {

    if (isLoading) {
      return;
    }

    setIsLoading(true);

    try {

      const conversation =
        await createConversation();


      const newConversation = {
        conversation_id:
          conversation.conversation_id,

        title: "New Conversation",

        created_at:
          conversation.created_at,
      };


      setConversations(
        (previous) => [
          newConversation,
          ...previous,
        ],
      );


      setConversationId(
        conversation.conversation_id,
      );

      setMessages([]);

    } catch (error) {

      console.error(
        "Failed to create conversation:",
        error,
      );

    } finally {

      setIsLoading(false);

    }

  }


  async function handleSelectConversation(
    id,
  ) {

    if (id === conversationId) {
      return;
    }

    setIsLoading(true);

    try {

      const conversation =
        await getConversation(id);


      setConversationId(id);


      const formattedMessages =
        conversation.messages || [];


      setMessages(
        formattedMessages.map(
          (message, index) => ({
            id:
              message.id ||
              `${id}-${index}`,

            role: message.role,

            content:
              message.content,

            sources:
              message.sources || [],
          }),
        ),
      );

    } catch (error) {

      console.error(
        "Failed to load conversation:",
        error,
      );

    } finally {

      setIsLoading(false);

    }

  }


  async function handleDeleteConversation(
    event,
    id,
  ) {

    event.stopPropagation();


    try {

      await deleteConversation(id);


      setConversations(
        (previous) =>
          previous.filter(
            (conversation) =>
              conversation.conversation_id !== id,
          ),
      );


      if (id === conversationId) {

        setConversationId(null);

        setMessages([]);

      }

    } catch (error) {

      console.error(
        "Failed to delete conversation:",
        error,
      );

    }

  }


  return (
    <aside className="sidebar">

      <div className="sidebar-header">

        <div className="brand">

          <div className="brand-icon">
            AI
          </div>

          <div>

            <h2>
              Knowledge AI
            </h2>

            <span>
              RAG Assistant
            </span>

          </div>

        </div>

      </div>


      <button
        className="new-chat-button"
        onClick={
          handleNewConversation
        }
        disabled={isLoading}
      >

        <span>
          +
        </span>

        New Conversation

      </button>


      <div className="sidebar-section">

        <div className="sidebar-section-title">

          Conversations

        </div>


        <div className="conversation-list">

          {conversations.length === 0 && (

            <div className="empty-conversations">

              No conversations yet

            </div>

          )}


          {conversations.map(
            (conversation) => (

              <div
                key={
                  conversation.conversation_id
                }

                className={
                  `conversation-item ${
                    conversation.conversation_id ===
                    conversationId
                      ? "active"
                      : ""
                  }`
                }

                onClick={() =>
                  handleSelectConversation(
                    conversation.conversation_id,
                  )
                }
              >

                <div className="conversation-icon">

                  💬

                </div>


                <div className="conversation-title">

                  {conversation.title ||
                    "New Conversation"}

                </div>


                <button
                  className="delete-conversation"

                  onClick={(event) =>
                    handleDeleteConversation(
                      event,
                      conversation.conversation_id,
                    )
                  }

                  aria-label={
                    "Delete conversation"
                  }
                >

                  ×

                </button>

              </div>

            ),
          )}

        </div>

      </div>


      <DocumentPanel />

    </aside>
  );

}


export default Sidebar;