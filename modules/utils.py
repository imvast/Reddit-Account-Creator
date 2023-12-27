import capsolver
import json

with open("./config.json", "r") as f:
    config = json.load(f)

capsolver.api_key = config.get("capsolver_key")


class Captcha:
    def _solve_recaptcha():
        solution: dict = capsolver.solve(
            {
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteURL": "https://www.reddit.com/",
                "websiteKey": "6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC",
            }
        )
        if token := solution.get("gRecaptchaResponse"):
            return token

        return Captcha._solve_recaptcha()
