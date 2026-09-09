import ReactMarkdown from "react-markdown";
import SourceCard from "./SourceCard";


function Message({
  message,
}) {

  const isUser =
    message.role === "user";


  return (
    <div
      className={
        `message-row ${
          isUser
            ? "user-message"
            : "assistant-message"
        }`
      }
    >

      {!isUser && (

        <div className="message-avatar">
          AI
        </div>

      )}


      <div className="message-content">

        <div className="message-role">

          {isUser
            ? "You"
            : "AI Assistant"}

        </div>


        <div
          className={
            `message-bubble ${
              message.isError
                ? "error-message"
                : ""
            }`
          }
        >

          {isUser ? (

            message.content

          ) : (

            <ReactMarkdown>
              {message.content || ""}
            </ReactMarkdown>

          )}

        </div>


        {!isUser &&
          message.sources?.length > 0 && (

          <div className="sources-container">

            <div className="sources-title">
              Sources
            </div>


            {message.sources.map(
              (source, index) => (

                <SourceCard
                  key={
                    source.document_id
                      ? `${source.document_id}-${source.page ?? "unknown"}`
                      : source.chunk_id ||
                        `${index}`
                  }

                  source={source}
                />

              ),
            )}

          </div>

        )}


        {!isUser &&
          message.cached && (

          <div className="message-meta">

            ⚡ Served from cache

          </div>

        )}

      </div>

    </div>
  );

}


export default Message;