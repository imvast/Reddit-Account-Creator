#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 12/13/2023
"""

from modules.cookies import RedditCookies
from modules.reddit import RedditMain
from modules.utils import Captcha

from concurrent.futures import ThreadPoolExecutor
from tls_client import Session
from terminut import log
from secrets import token_hex
from random import choice
from signal import signal, SIGINT
from json import load
from time import sleep
from os import _exit



def main():
    session = Session(client_identifier="firefox_121", random_tls_extension_order=True)
    
    proxy = choice(proxies)
    session.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    session.cookies = RedditCookies(session)()
    
    reddit = RedditMain(session)

    capKey = Captcha._solve_recaptcha()
    log.debug(f"Captcha Solved. [{capKey[:25]}...]")

    username = reddit.getUsernames().json().get("data").get("generatedUsernames")[0]
    if not username:
        log.error("could not generate username")
        return
    
    email = f"{token_hex(6)}@tempmail.cc"

    res = reddit.register(capKey, email, username)
    if "reddit_session" in res.cookies:
        log.log("Account Created.", Username=username, Email=email)
        open("./created.txt", "a+").write(
            f"{username}:{email}:t]@9kYz)yCjys9V:{res.cookies.get('reddit_session')}"
        )

    elif "BAD_CAPTCHA" in res.text:
        log.error("ur solver sucks lil bro")
    elif "RATELIMIT" in res.text:
        log.error("ratelimit?? what a loser")
    else:
        print(res.text, res.status_code)


if __name__ == "__main__":
    signal(SIGINT, lambda *_: (log.fatal("Keyboard Interrupt Detected."), _exit(0)))

    config = load(open("./config.json", "r"))
    proxies = [i.strip() for i in open("./proxies.txt", "r")]
    executor = ThreadPoolExecutor(max_workers=config.get("threads"))

    if not proxies:
        log.fatal("no proxies found")
        _exit(-136312)

    while True:
        executor.submit(main)
        sleep(.1)
