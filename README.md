# YouTube Transcript API Server

A powerful, self-hosted, and ready-to-deploy API server built with FastAPI to fetch transcripts from any YouTube video. This project is containerized using Docker and managed with Docker Compose, making it incredibly easy to deploy and run.

## ✨ Features

- **🚀 High Performance:** Built with **FastAPI** for fast and reliable API responses.
- **📦 Docker Ready:** Comes with pre-configured `Dockerfile` and `docker-compose.yml` for seamless deployment and local development.
- **📝 Professional Logging:** Detailed logging is built-in, writing to both the console and a rotating `api.log` file for easy monitoring and debugging.
- **🔑 No API Keys Needed:** Leverages the robust `youtube-transcript-api` library which does not require any YouTube API keys.
- **📚 Interactive Docs:** Automatic, interactive API documentation provided by FastAPI (via Swagger UI) at the `/docs` endpoint.

## ⚙️ API Endpoints

Once the server is running, you can access the following endpoints:

### Interactive API Docs

For a full, interactive documentation of the API, visit:
```
http://<your_server_ip>:5000/docs
```

### Get Transcript

Fetches the transcript for a specific video. You can specify one or more languages in order of preference.

- **Endpoint:** `GET /transcript/{video_id}`
- **Example Request:**
  ```bash
  curl "http://127.0.0.1:5000/transcript/x4fEnyINwdw?languages=ar&languages=en"
  ```
- **Success Response (200):**
  ```json
  {
    "video_id": "x4fEnyINwdw",
    "transcript": [
      {
        "text": "احنا بقينا في عصر جديد ...",
        "start": 0.08,
        "duration": 4.4
      },
      // ... more transcript parts
    ]
  }
  ```

### List Available Transcripts

Lists all available transcript languages for a given video. This is useful to check before requesting a specific transcript.

- **Endpoint:** `GET /transcripts/list/{video_id}`
- **Example Request:**
  ```bash
  curl http://127.0.0.1:5000/transcripts/list/x4fEnyINwdw
  ```
- **Success Response (200):**
  ```json
  {
    "video_id": "x4fEnyINwdw",
    "available_transcripts": [
      {
        "language": "Arabic",
        "language_code": "ar",
        "is_generated": true,
        "is_translatable": true
      }
    ]
  }
  ```

## 🚀 Deployment & Local Development

### Using Docker Compose (Recommended)

This is the easiest way to get the server running on both your local machine and a production server.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/amrpyt/youtube-transcript-api-project.git
    cd youtube-transcript-api-project
    ```
2.  **Run the server:**
    ```bash
    docker-compose up -d --build
    ```
3.  The API will now be running on port `5000`. To see logs, run `docker-compose logs -f`.
4.  To stop the server, run `docker-compose down`.

### Deployment with Coolify

This project is perfectly set up for one-click deployment with [Coolify](https://coolify.io/).

1.  Connect your GitHub account to Coolify.
2.  Create a new "Application" resource and point it to this repository.
3.  Coolify will automatically detect the `Dockerfile` or `docker-compose.yml`.
4.  Set the port to `5000`.
5.  Click **Deploy**. That's it!

---
_This project was set up by an AI assistant._
