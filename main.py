# main.py
import os
import re
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.auth import OAuthSettings
from youtube_transcript_api import YouTubeTranscriptApi
from utils.auth import create_auth0_verifier

load_dotenv()

# استدعاء المتغيرات البيئية التي سنضعها لاحقاً في منصة الاستضافة
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
RESOURCE_SERVER_URL = os.getenv("RESOURCE_SERVER_URL")

# إعدادات المصادقة (Auth0)
token_verifier = create_auth0_verifier(
    auth0_domain=AUTH0_DOMAIN,
    audience=RESOURCE_SERVER_URL
)

oauth_settings = OAuthSettings(
    issuer_url=f"https://{AUTH0_DOMAIN}/",
    resource_server_url=RESOURCE_SERVER_URL,
    required_scopes=["read:youtube_transcripts"] # ChatGPT يتطلب تحديد Scopes
)

# تهيئة السيرفر على منفذ عام (0.0.0.0) مع إضافة طبقة الحماية
mcp = FastMCP(
    name="YouTube-MCP-Remote",
    instructions="Use this server to fetch YouTube transcripts.",
    host="0.0.0.0", 
    token_verifier=token_verifier,
    oauth_settings=oauth_settings
)

@mcp.tool()
def fetch_video_transcript(url: str) -> str:
    """Fetches the transcript of a YouTube video given its URL."""
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if not video_id_match: return "Error: Invalid YouTube URL."
    video_id = video_id_match.group(1)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([f"[{t['start']:.2f}] {t['text']}" for t in transcript])
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

if __name__ == "__main__":
    mcp.run()