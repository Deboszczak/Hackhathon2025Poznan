from uagents import Agent, Context, Model


class Message(Model):
    message: str


RECIPIENT_ADDRESS = (
    "agent1qvhjetpz8x436d64xq9fh8lkd6g7w3qujs5rzu6d4emqj3zga28tw67mz4s"
)

SenderAgent = Agent(
    name="SenderAgent",
    port=8000,
    seed="SenderAgent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

print(SenderAgent.address)

waiting_for_response = False

with open('prompt.txt', 'r') as file:
    content = file.read()
FIRST_MESSAGE = content  # Initial question to send

@SenderAgent.on_message(model=Message)
async def handle_response(ctx: Context, sender: str, msg: Message):
    global waiting_for_response
    ctx.logger.info(f"\n\n{msg.message}\n\n")
    waiting_for_response = False  # Allow sending the next message
    await send_next_message(ctx)


async def send_next_message(ctx: Context):
    global waiting_for_response
    if not waiting_for_response:  # Ensure only one message at a time
        user_input = input("Enter your message to send: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            ctx.shutdown()  # Graceful exit mechanism
            return

        await ctx.send(RECIPIENT_ADDRESS, Message(message=user_input))
        waiting_for_response = True

@SenderAgent.on_event("startup")
async def start_interaction(ctx: Context):
    global waiting_for_response
    # Send the initial message without waiting for user input
    await ctx.send(RECIPIENT_ADDRESS, Message(message=FIRST_MESSAGE))
    waiting_for_response = True


if __name__ == "__main__":
    SenderAgent.run()
