import os

def is_first_launch(user_dir: str) -> bool:
    return not os.path.exists(user_dir)