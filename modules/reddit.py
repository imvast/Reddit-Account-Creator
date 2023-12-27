#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 12/23/2024
"""

from tls_client import Session
from terminut import log


class RedditMain:
    def __init__(self, client: Session) -> None:
        self.client = client
        self.common_headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Origin": "https://www.reddit.com",
            "Referer": "https://www.reddit.com/?rdt=54309",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        }

    def get_usernames(self):
        url = "https://www.reddit.com/svc/shreddit/graphql"

        headers = {
            **self.common_headers,
            "Content-Type": "application/json",
            "Host": "www.reddit.com",
        }

        payload = {
            "operation": "GeneratedUsernames",
            "variables": {"count": 10},
            "csrf_token": self.client.cookies.get("csrf_token"),
        }

        return self.client.post(url, headers=headers, json=payload)

    def Register(self, cap_token, email, username):
        headers = {
            **self.common_headers,
            "content-type": "application/x-www-form-urlencoded",
        }

        data = {
            "gRecaptchaResponse": cap_token,
            "email": email,
            "username": username,
            "password": "t]@9kYz)yCjys9V",
            "csrf_token": self.client.cookies.get("csrf_token"),
        }

        return self.client.post(
            "https://www.reddit.com/svc/shreddit/account/register",
            headers=headers,
            data=data,
        )
