import demo.demo_process as demo_process
from demo.logging_handler import initialize_logging

if __name__ == "__main__":
    initialize_logging()
    demo_process.start()