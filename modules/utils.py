import capsolver
import json

capsolver.api_key = json.load(open("./config.json", "r")).get("capsolver_key")

class Captcha:
    def _solve_recaptcha():
        solution: dict = capsolver.solve({
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": "https://www.reddit.com/",
            "websiteKey": "6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC",
        })

        if token := solution.get("gRecaptchaResponse"):
            return token

        return Captcha._solve_recaptcha()