#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 12/23/2024
"""

from tls_client import Session


class RedditCookies:
    def __init__(self, client: Session) -> None:
        self.client = client
        self.common_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Host": "www.reddit.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        }

    def get_cookies(self) -> dict:
        headers = {
            **self.common_headers,
        }

        response = self.client.get("https://www.reddit.com/", headers=headers) # this also returns the rdt id but i think it doenst matter ['location']
        first_cookies = response.cookies  # rdt | edgebucket
        
        response = self.client.get(
            "https://www.reddit.com/?rdt=54309", headers=headers, cookies=first_cookies
        )
        second_cookies = response.cookies  # loid | session_tracker | csrf_token | token_v2 | csv

        all_cookies = first_cookies
        all_cookies.update(second_cookies)
        
        return all_cookies