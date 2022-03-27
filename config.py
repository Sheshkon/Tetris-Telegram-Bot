import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.environ['TOKEN']
URL_GAME_SITE = 'https://sheshkon.github.io/tetris-site/'
ADMINS_ID = (int(os.environ['ADMIN_ID_1']), int(os.environ['ADMIN_ID_2']))
DB_URI = os.environ['DB_URI']
PRIVATE_KEY = os.environ['PRIVATE_KEY']
START_TEXT = "Hi!\nI'm Tetris Bot!\nUse /help command to see list of commands."
LOG_ID = os.environ['LOG_ID']
URL_WEB_GAME = 'https://sheshkon.github.io/web_tetris'

RULES_TEXT = '<b>Goals</b>\n\n' \
             '   The aim in Tetris is simple; you bring down\n' \
             'block from the top of the screen. You can \n' \
             'move the blocks around, either left to right\n' \
             'and/or you can rotate them. The blocks fall\n' \
             'at a certain rate, but you can make them fall\n' \
             'faster if you’re sure of your positioning.\n\n' \
             '   Your objective is to get all the blocks to\n' \
             'fill all the empty space in a line at the \n' \
             'bottom of the screen;whenever you do this,\n' \
             ' you’ll find that the blocks vanish and you\n' \
             'get awarded some points.\n\n' \
             '<b>Rules</b>\n\n' \
             '   Tetris has very simple rules: you can only \n' \
             'move the pieces in specific ways; your game\n' \
             'is over if your pieces reach the top of the\n' \
             'screen; and you can only remove pieces from\n' \
             'the screen by filling all the blank space in\n' \
             'a line.\n\n' \
             '   Rules give much needed structure to our play.\n' \
             'A completely random environment offers no clue\n' \
             'as to how to play and would be incredibly\n' \
             'frustrating. How fortunate it is, then, that\n' \
             'Tetris’s three rules are what shape it into such\n' \
             'an award-winning game.'

HELP_TEXT = '<b>List of commands:</b>\n' \
            '/start - start bot\n' \
            '/help - show list of commands\n' \
            '/get_latest_update - latest version of the game\n' \
            '/web - web version\n' \
            '/site - site link\n' \
            '/leaderboard - leaders scores\n' \
            '/rules - show rules of the game\n' \
            '/about - show authors\n' \
            '/screenshots - show gameplay screenshots\n' \
            '<i>Admin commands:</i>\n' \
            '<i>/send_all - send text message for all users</i>\n' \
            '<i>/send_update - send new update to all users</i>'

ABOUT_TEXT = "It is a bot for multiplayer tetris game created by <a " \
             "href='https://github.com/vitaliysheshkoff/Tetris-Multiplayer'><span class='tg-spoiler'>Author link</span></a> "

SCREENSHOTS_LINKS = ('https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/resize_network_multiplayer_branch/screenshots/image_2021-12-31_23-44-31.png',
                     'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/resize_network_multiplayer_branch/screenshots/image_2021-12-31_23-27-22.png',
                     'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/resize_network_multiplayer_branch/screenshots/image_2021-12-31_23-20-26.png',
                     'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/resize_network_multiplayer_branch/screenshots/image_2021-12-31_23-21-18.png',
                     'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/resize_network_multiplayer_branch/screenshots/image_2021-12-31_23-25-15.png',
                     'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/resize_network_multiplayer_branch/screenshots/image_2022-01-01_00-13-54.png')
