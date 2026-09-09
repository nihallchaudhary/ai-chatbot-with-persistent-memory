import {
  useEffect,
  useRef,
  useState,
} from "react";


function ChatInput({
  onSend,
  disabled,
}) {

  const [value, setValue] =
    useState("");

  const textareaRef =
    useRef(null);


  useEffect(() => {

    if (!textareaRef.current) {
      return;
    }

    textareaRef.current.style.height =
      "auto";

    textareaRef.current.style.height =
      `${Math.min(
        textareaRef.current.scrollHeight,
        160,
      )}px`;

  }, [value]);


  function handleSubmit(event) {

    event.preventDefault();

    const message =
      value.trim();

    if (!message || disabled) {
      return;
    }

    onSend(message);

    setValue("");

  }


  function handleKeyDown(event) {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      handleSubmit(event);

    }

  }


  return (
    <div className="chat-input-wrapper">

      <form
        className="chat-input-form"
        onSubmit={handleSubmit}
      >

        <textarea
          ref={textareaRef}

          value={value}

          onChange={(event) =>
            setValue(event.target.value)
          }

          onKeyDown={handleKeyDown}

          placeholder={
            disabled
              ? "AI is thinking..."
              : "Ask anything about your documents..."
          }

          disabled={disabled}

          rows="1"
        />


        <button
          type="submit"

          disabled={
            disabled ||
            !value.trim()
          }

          aria-label="Send message"
        >

          ↑

        </button>

      </form>


      <p className="input-hint">

        Press Enter to send ·
        Shift + Enter for a new line

      </p>

    </div>
  );

}


export default ChatInput;