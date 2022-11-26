#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py: This script adds friends from your suggestion list until limit.
"""


from os.path import exists
from vk_api import vk_api


def init_bot() -> None:
    """
    init_bot: Initializes bot via entering login and password, getting
    access token, saving it into file 'access_token.txt'.
    """
    while True:
        try:
            session = vk_api.VkApi(
                login=input('Login: '),
                password=input('Password: '),
                scope=65538  # 65536 for non-expiring token, 2 for friends
            )

            session.auth(token_only=True)

            with open('access_token.txt', 'w') as ftoken:
                ftoken.write(session.token.get('access_token'))

        except Exception:
            print('Wrong Login or Password.')

        else:
            break


if __name__ == '__main__':
    if not exists('access_token.txt'):
        init_bot()

    access_token = open('access_token.txt').readline()
    session = vk_api.VkApi(token=access_token)
    method = vk_api.VkApiMethod(session)

    while True:
        try:
            suggestions = method.friends.getSuggestions(filter='mutual')

            for user in suggestions.get('items'):
                method.friends.add(user_id=user.get('id'))

        except vk_api.ApiError as error:
            if error.code == 9:
                print('You have reached the limit for today.')
                break

        except Exception:
            ...
