import {
  useRef,
  useState,
} from "react";

import {
  uploadDocument,
} from "../services/api";


function DocumentPanel() {

  const inputRef =
    useRef(null);

  const [isUploading, setIsUploading] =
    useState(false);

  const [uploadedDocuments,
    setUploadedDocuments] =
    useState([]);

  const [error, setError] =
    useState(null);


  function handleChooseFile() {

    if (isUploading) {
      return;
    }

    inputRef.current?.click();

  }


  async function handleFileChange(
    event,
  ) {

    const file =
      event.target.files?.[0];


    if (!file) {
      return;
    }


    if (
      file.type !==
      "application/pdf"
    ) {

      setError(
        "Only PDF files are supported.",
      );

      return;

    }


    setError(null);

    setIsUploading(true);


    try {

      const result =
        await uploadDocument(file);


      setUploadedDocuments(
        (previous) => [
          {
            id:
              result.document_id ||
              crypto.randomUUID(),

            filename:
              result.filename ||
              file.name,

            chunks:
              result.chunks_stored ||
              result.chunks_created ||
              0,
          },

          ...previous,
        ],
      );


    } catch (error) {

      setError(
        error.message ||
        "Failed to upload document.",
      );

    } finally {

      setIsUploading(false);

      event.target.value = "";

    }

  }


  return (
    <div className="document-panel">

      <div className="sidebar-section-title">

        Documents

      </div>


      <input
        ref={inputRef}

        type="file"

        accept=".pdf,application/pdf"

        onChange={
          handleFileChange
        }

        hidden
      />


      <button
        className="upload-document-button"

        onClick={
          handleChooseFile
        }

        disabled={
          isUploading
        }
      >

        <span className="upload-icon">

          {isUploading
            ? "⏳"
            : "↑"}

        </span>


        {isUploading
          ? "Processing..."
          : "Upload PDF"}

      </button>


      {error && (

        <div className="upload-error">

          {error}

        </div>

      )}


      <div className="uploaded-document-list">

        {uploadedDocuments.map(
          (document) => (

            <div
              className="uploaded-document"
              key={document.id}
            >

              <span className="document-icon">

                📄

              </span>


              <div className="document-info">

                <div className="document-name">

                  {document.filename}

                </div>


                <div className="document-meta">

                  {document.chunks} chunks

                </div>

              </div>

            </div>

          ),
        )}

      </div>


      {uploadedDocuments.length === 0 &&
        !isUploading && (

        <div className="no-documents">

          Upload documents to start
          asking questions.

        </div>

      )}

    </div>
  );

}


export default DocumentPanel;