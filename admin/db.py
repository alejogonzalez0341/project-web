from dotenv import dotenv_values


config_env= dotenv_values(".env")

USERNAME = config_env["USERNAME"]
PASSWORD= config_env["PASSWORD"]
EMAIL= config_env["EMAIL"]
FULLNAME= config_env["FULLNAME"]

admin_user_db= {
    "gregory":{
        "username": USERNAME,
        "fullname": FULLNAME,
        "email": EMAIL,
        "password": PASSWORD,
        "disabled": False
    },
}

