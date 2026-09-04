import time
import random

from google.genai import errors

# Transient errors worth retrying: 429 rate limit, 500 internal, 503 overloaded.
RETRYABLE_CODES = {429, 500, 503}

# Fixed fallback chain. These are the only Google models with usable free-tier
# limits (15 RPM, 250K TPM, 500 RPD); every other model has zero quota or
# crashes once free usage is exhausted, so the chain is intentionally not
# configurable by the caller.
FALLBACK_MODELS = ("gemini-3.5-flash-lite", "gemini-3.1-flash-lite")

# How many full loops over FALLBACK_MODELS we allow before giving up. The
# rotation is circular (once past the last model we wrap back to the first),
# because a 429 is a *per-minute* quota that renews over time, so a model that
# failed earlier may work again after we spent time on the others. This cap is
# the stop condition that keeps "everything is down" from looping forever.
MAX_CYCLES = 2

# Sticky pointer to the model currently in use. Since generate_content_resilient
# is called once per job row (in both the summarize and the score loop), keeping
# this at module level means once a model is known-good we start from it on every
# subsequent row instead of re-probing a dead model each time. It only moves when
# the current model exhausts its retries.
_current_model_idx = 0


def generate_content_resilient(client, *, contents, config,
                               max_retries=5, base_delay=2.0):
    """Call the Gemini API with retry + backoff and sticky, circular fallback.

    Starts from the last model known to work (`_current_model_idx`). The current
    model is retried up to `max_retries` times with exponential backoff (plus
    jitter) on transient errors; if it stays down we rotate to the next model,
    wrapping around the list. A successful call updates the sticky pointer so the
    next row starts from that model directly. Rotation is bounded by MAX_CYCLES
    full loops over the list, after which the last transient error is re-raised.
    Non-transient errors (400, 401, 404, ...) are raised immediately.
    """
    global _current_model_idx
    last_exc = None
    n = len(FALLBACK_MODELS)

    for rotation in range(n * MAX_CYCLES):
        idx = (_current_model_idx + rotation) % n
        model = FALLBACK_MODELS[idx]
        for attempt in range(max_retries):
            try:
                resp = client.models.generate_content(
                    model=model, contents=contents, config=config
                )
                _current_model_idx = idx  # remember the model that worked
                return resp
            except errors.APIError as e:
                if e.code not in RETRYABLE_CODES:
                    raise
                last_exc = e
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                print(f"[llm] {model} -> {e.code}, attempt "
                      f"{attempt + 1}/{max_retries}, waiting {delay:.1f}s",
                      flush=True)
                time.sleep(delay)
        print(f"[llm] {model} exhausted, rotating to next model...", flush=True)

    raise last_exc
