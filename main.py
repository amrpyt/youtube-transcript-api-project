import logging
import logging.config
import sys
from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# --- Logging Configuration ---
# A dictionary configuring the logging.
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "api.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "default",
        },
    },
    "loggers": {
        "api_logger": {  # Our custom logger
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Get our custom logger
logger = logging.getLogger("api_logger")


# --- FastAPI App ---
app = FastAPI(
    title="YouTube Transcript API",
    description="An API to fetch transcripts from YouTube videos, using the youtube-transcript-api library.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete.")
    logger.info("Log files will be written to api.log")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown.")


@app.get("/", tags=["General"])
async def read_root():
    """
    A welcome message for the API.
    """
    logger.info("Root endpoint was accessed.")
    return {"message": "Welcome to the YouTube Transcript API. Go to /docs for documentation."}


@app.get("/transcript/{video_id}", tags=["Transcripts"])
async def get_transcript(
    video_id: str,
    languages: list[str] = Query(default=['en'], description="A list of language codes to search for in order of preference (e.g., 'en', 'es', 'de').")
):
    """
    Fetches the transcript for a given YouTube video ID.
    
    You can provide multiple language codes, and it will try to find a transcript in that order.
    """
    logger.info(f"Received request for transcript of video_id: '{video_id}' with languages: {languages}")
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        logger.info(f"Successfully fetched transcript for video_id: '{video_id}'")
        return {"video_id": video_id, "transcript": transcript_list}
    except NoTranscriptFound:
        logger.warning(f"No transcript found for video_id: '{video_id}' in languages: {', '.join(languages)}")
        try:
            available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
            available_codes = [t.language_code for t in available_transcripts]
            error_detail = (
                f"Could not find a transcript in the requested languages: {', '.join(languages)}. "
                f"Available languages are: {', '.join(available_codes)}"
            )
            logger.info(f"Found available transcripts for video_id: '{video_id}': {', '.join(available_codes)}")
            raise HTTPException(status_code=404, detail=error_detail)
        except TranscriptsDisabled:
            logger.error(f"Transcripts are disabled for video '{video_id}'.")
            raise HTTPException(status_code=403, detail=f"Transcripts are disabled for video '{video_id}'.")
    except TranscriptsDisabled:
        logger.error(f"Transcripts are disabled for video '{video_id}'.")
        raise HTTPException(status_code=403, detail=f"Transcripts are disabled for video '{video_id}'.")
    except Exception as e:
        logger.critical(f"An unexpected error occurred for video_id '{video_id}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/transcripts/list/{video_id}", tags=["Transcripts"])
async def list_transcripts(video_id: str):
    """
    Lists all available transcripts for a given YouTube video ID.
    This is useful for finding out which languages are available for a video before requesting a transcript.
    """
    logger.info(f"Received request to list transcripts for video_id: '{video_id}'")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # The transcript object is not directly JSON serializable, so we format it.
        formatted_list = [
            {
                "language": t.language,
                "language_code": t.language_code,
                "is_generated": t.is_generated,
                "is_translatable": t.is_translatable,
            }
            for t in transcript_list
        ]
        logger.info(f"Successfully listed {len(formatted_list)} available transcripts for video_id: '{video_id}'")
        return {"video_id": video_id, "available_transcripts": formatted_list}
    except TranscriptsDisabled:
        logger.error(f"Transcripts are disabled for video '{video_id}'.")
        raise HTTPException(status_code=403, detail=f"Transcripts are disabled for video '{video_id}'.")
    except Exception as e:
        logger.critical(f"An unexpected error occurred while listing transcripts for video_id '{video_id}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
