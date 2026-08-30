import time
import random

from google.genai import errors

# Transient errors worth retrying: 429 rate limit, 500 internal, 503 overloaded.
RETRYABLE_CODES = {429, 500, 503}


def generate_content_resilient(client, *, contents, config, models,
                               max_retries=5, base_delay=2.0):
    """Call the Gemini API with retry + backoff and model fallback.

    `models` is an ordered list, e.g. ["gemini-2.5-flash-lite", "gemini-2.0-flash"].
    Each model is retried up to `max_retries` times with exponential backoff
    (plus jitter) on transient errors before falling back to the next model.
    Non-transient errors (400, 401, 404, ...) are raised immediately. If every
    model is exhausted, the last transient error is re-raised.
    """
    last_exc = None
    for model in models:
        for attempt in range(max_retries):
            try:
                return client.models.generate_content(
                    model=model, contents=contents, config=config
                )
            except errors.APIError as e:
                if e.code not in RETRYABLE_CODES:
                    raise
                last_exc = e
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"[llm] {model} -> {e.code}, attempt "
                      f"{attempt + 1}/{max_retries}, waiting {delay:.1f}s",
                      flush=True)
                time.sleep(delay)
        print(f"[llm] {model} exhausted, falling back to next model...",
              flush=True)
    raise last_exc
