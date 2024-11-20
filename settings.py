from environs import Env

env = Env()
env.read_env()
    

class Settings:
    HOST = env.str("HOST")
    DATABASE = env.str("DATABASE")
    USER = env.str("USER")
    PASSWORD = env.str("PASSWORD")
    BACKEND = env.str("BACKEND")
	

def get_settings():
	return Settings()