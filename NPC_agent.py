from uagents import Agent, Context, Model
from openai import OpenAI

# OpenAI client (Replace "KEY" with your actual API key)
client = OpenAI(api_key="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")

# Message Model
class Message(Model):
    message: str

# Define the AI agent
AI_Agent = Agent(
    name="AI_Agent",
    port=8001,
    seed="AI_Agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

print(AI_Agent.address)

conversation_history = []

def generate_response(user_message):
    conversation_history.append({"role": "user", "content": user_message})
    prompt = "You are a helpful assistant."  # Default persona
    messages = [{"role": "system", "content": prompt}] + conversation_history
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-4" if available
            messages=messages
        )
        ai_reply = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": ai_reply})
        return ai_reply
    except Exception as e:
        return f"An error occurred: {str(e)}"

@AI_Agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    ai_reply = generate_response(msg.message)
    await ctx.send(sender, Message(message=ai_reply))

if __name__ == "__main__":
    AI_Agent.run()
