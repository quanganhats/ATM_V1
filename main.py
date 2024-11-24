import uvicorn
import sys


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    uvicorn.run("app.app:app", host='0.0.0.0', port=port,
                log_level="info", reload=True)
