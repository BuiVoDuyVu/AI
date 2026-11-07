from openai import AuthenticationError, OpenAI, RateLimitError
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

api_key = os.getenv("OPEN_API_KEY")
if not api_key or not api_key.strip():
    raise SystemExit("Thieu OPEN_API_KEY. Hay them API key that vao file .env.")
api_key = api_key.strip()


client = OpenAI(
    api_key = api_key    
)
user_input = input("Enter your prompt: ")
current_time = datetime.now().astimezone()
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Respond in the user's language. "
                    "The current local date and time on the user's computer is "
                    f"{current_time.isoformat(timespec='seconds')}. "
                    "When asked about the current local time or date, use this "
                    "timestamp and its UTC offset. This timestamp comes from "
                    "the computer clock, not an internet lookup."
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
except AuthenticationError:
    raise SystemExit(
        "API key khong hop le (401). Kiem tra OPEN_API_KEY trong file .env "
        "hoac tao key moi tai https://platform.openai.com/api-keys."
    ) from None
except RateLimitError as error:
    if error.code in {"insufficient_quota", "credit_balance_exhausted"} or "no credits remaining" in str(error).lower():
        raise SystemExit(
            "Tai khoan API khong du credit/quota. Kiem tra va nap credit tai: "
            "https://platform.openai.com/settings/organization/billing/"
        ) from None
    raise SystemExit(
        f"API tu choi yeu cau (429): {error.message}"
    ) from None
answer = response.choices[0].message.content
print(answer)
