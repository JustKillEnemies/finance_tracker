from environs import Env


def get_db_data(path: str | None = None):
    env = Env()
    env.read_env(path)
    return [env("DB_NAME"), env('DB_USER'), env("DB_PASSWORD"), env('DB_HOST'), env('DB_PORT')]

def get_email_data(path: str | None = None):
    env = Env()
    env.read_env(path)
    return [env("EMAIL_HOST_PASSWORD"), env("EMAIL_HOST"), env("EMAIL_PORT"),
            env("EMAIL_HOST_USER"), env("EMAIL_USE_TLS")]
