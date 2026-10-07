import re
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi

# تهيئة سيرفر FastMCP كما ظهر في الدرس
mcp = FastMCP("YouTube-MCP-Server")

@mcp.tool()
def fetch_video_transcript(url: str) -> str:
    """
    Fetches the transcript of a YouTube video given its URL. 
    Use this tool FIRST whenever the user provides a YouTube link.
    """
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if not video_id_match:
        return "Error: Invalid YouTube URL."
    
    video_id = video_id_match.group(1)
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatted_transcript = "\n".join([f"[{t['start']:.2f}] {t['text']}" for t in transcript])
        return formatted_transcript
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

@mcp.tool()
def fetch_instructions(task_name: str) -> str:
    """
    Fetches specific prompt instructions for tasks. 
    Available task_name options: 'write_video_chapters'.
    Use this tool to know exactly HOW to format your response.
    """
    try:
        with open(f"prompts/{task_name}.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: No specific instructions found for {task_name}."

if __name__ == "__main__":
    mcp.run()