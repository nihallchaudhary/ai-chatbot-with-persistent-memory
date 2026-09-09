import { useState } from "react";

import ChatWindow from "./components/ChatWindow";
import Sidebar from "./components/Sidebar";


function App() {

  const [
    conversationId,
    setConversationId,
  ] = useState(null);

  const [
    messages,
    setMessages,
  ] = useState([]);

  const [
    conversations,
    setConversations,
  ] = useState([]);

  return (
    <div className="app">

      <Sidebar
        conversations={
          conversations
        }
        setConversations={
          setConversations
        }
        conversationId={
          conversationId
        }
        setConversationId={
          setConversationId
        }
        setMessages={
          setMessages
        }
      />

      <main className="main-content">

        <ChatWindow
          conversationId={
            conversationId
          }
          setConversationId={
            setConversationId
          }
          messages={messages}
          setMessages={
            setMessages
          }
        />

      </main>

    </div>
  );
}


export default App;