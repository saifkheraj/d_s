**Best Practices for Exception Handling (Summary)**

* **Handle exceptions at the right level:** Keep exception handling consistent with the function’s responsibility. For example, `ConnectionError` should be handled inside the connection logic, not where data is decoded.
* **Do not expose tracebacks to users:** Log detailed errors internally, but show generic error messages like “Something went wrong” to prevent security risks.
* **Avoid empty `except` blocks:** Never silence errors with `pass`; instead, catch specific exceptions and handle them properly (e.g., log, retry, or raise a new one).
* **Catch specific exceptions:** Use targeted exceptions like `KeyError` or `ValueError` instead of a broad `Exception`.
* **Include the original exception:** When re-raising, use `raise NewError(...) from e` to preserve context for debugging.
* **Use `contextlib.suppress()`** explicitly if you need to ignore certain exceptions intentionally.



from contextlib import suppress

class CustomError(Exception):
    pass

def connect():
    raise ConnectionError("Failed to connect")

def decode():
    raise ValueError("Bad data format")

def main():
    try:
        connect()
    except ConnectionError as e:
        print("Retrying connection...")   # ✅ Right level of abstraction

    try:
        decode()
    except ValueError as e:
        print("Something went wrong")     # ✅ Generic message, no traceback

    try:
        raise KeyError("Missing key")
    except KeyError as e:
        print(f"Handled specific: {e}")   # ✅ Catch specific exception

    try:
        raise TypeError("Wrong type")
    except TypeError as e:
        raise CustomError("Custom wrapper") from e   # ✅ Include original exception

    with suppress(ZeroDivisionError):               # ✅ Explicitly ignore
        1 / 0

    try:
        pass  # no empty except ✅ Avoid empty block
    except Exception:
        pass

main()
