from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup

buttons_kb = [
    InlineKeyboardButton('🌐 Website', url='https://google.com'),
    InlineKeyboardButton('💩 PooCoin', url='https://poocoin.app/'),
    InlineKeyboardButton('🥞 PancakeSwap',
                         url='https://pancakeswap.finance/'),
    InlineKeyboardButton('Click here to prove you`re human', callback_data='confirm')
]

button_prove = InlineKeyboardButton('Click here', callback_data='confirm')

inject_buttons = InlineKeyboardMarkup(row_width=2).add(*buttons_kb)
inject_prove = InlineKeyboardMarkup().add(button_prove)