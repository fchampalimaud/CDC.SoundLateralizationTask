from shutdown.shutdown_script import Shutdown


def main():
    Shutdown()
    try:
        Shutdown(is_backup=True)
    except Exception:
        print("It was not possible to convert the output in the backup directory.")
