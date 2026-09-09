function SourceCard({
  source,
}) {

  const filename =
    source.filename ||
    "Unknown document";


  return (
    <div className="source-card">

      <div className="source-icon">
        📄
      </div>


      <div className="source-information">

        <div className="source-filename">

          {filename}

        </div>


        <div className="source-details">

          {source.page &&
            `Page ${source.page}`}

          {source.score !== null &&
            source.score !== undefined && (
              <>
                {" · "}
                Score:{" "}
                {Number(
                  source.score,
                ).toFixed(2)}
              </>
            )}

        </div>

      </div>

    </div>
  );

}


export default SourceCard;