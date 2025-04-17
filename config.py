from modules.blum.main import BlumModule
from modules.clayton.main import ClaytonModule

port = 50325

accounts_file = 'data/serial_numbers.txt'

modules_data = {
    #
    "blum": {
        "class": BlumModule,
        "domain": "blum",
        "appname": "app",
        "iframe_selector": "iframe.payment-verification",
        "referral_codes": ["ref_NrOGHTSwQw", ]
    },
    "clayton": {
        "class": ClaytonModule,
        "domain": "claytoncoinbot",
        "appname": "game",
        "iframe_selector": "iframe.payment-verification",
        "referral_codes": ["7267714184", ]
    },
}