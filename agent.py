import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

# 1. تحميل المفاتيح (سيقرأ OPENAI_API_KEY تلقائياً)
load_dotenv()

async def main():
    print("🔌 Starting Custom YouTube MCP Server & OpenAI Agent...")

    # 2. تشغيل السيرفر المخصص الخاص بنا (youtube_mcp_server.py) محلياً
    async with MCPServerStdio(
        params={
            "command": "python",
            # هنا نخبر النظام بتشغيل ملف السيرفر الذي كتبناه للتو
            "args": ["youtube_mcp_server.py"],
            "env": os.environ.copy()
        }
    ) as youtube_server:

        # 3. قراءة الإرشادات الأساسية
        agent_instructions = "You are a YouTube video assistant."
        if os.path.exists("system_instructions.md"):
            with open("system_instructions.md", "r", encoding="utf-8") as f:
                agent_instructions = f.read()

        # 4. بناء الوكيل (اعتماد كلي على OpenAI)
        youtube_agent = Agent(
            name="YouTube Video Assistant",
            model="gpt-4o",  # النموذج الأصلي من OpenAI
            instructions=agent_instructions,
            mcp_servers=[youtube_server]  # ربط الوكيل بسيرفر الـ MCP المحلي
        )

        print("\n✅ YouTube Agent is ready! (Waiting for a YouTube link...)\n")
        print("-" * 50)

        # 5. حلقة المحادثة
        input_items = []
        while True:
            try:
                user_input = input("\n💬 You: ")
                if user_input.lower() in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break
                if not user_input.strip(): continue

                input_items.append({"role": "user", "content": user_input})
                print("🤖 Agent is processing (Calling OpenAI & checking MCP tools)... ", end="", flush=True)

                # تنفيذ الأوامر، سيقوم النموذج بطلب الأدوات من السيرفر إذا احتاجها
                result = await Runner.run(youtube_agent, input_items)
                
                print(f"\n🤖 Agent:\n{result.final_output}")
                input_items.append({"role": "assistant", "content": result.final_output})

            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())