import re

verb = re.compile(r'^VB.?$')
music = re.compile(r'.*(mp3)$')
youtube = re.compile(r'youtube', re.IGNORECASE)
question = re.compile(r'^(wh(at|o|om|ose|ich|en|ere|y)|how)', re.IGNORECASE)
swearing = re.compile(r'ass(hole)?|bitch|cunt|dick|(mother)?fuck(er)?|kike|moist|nigg(a|er)?|pussy|bugger|bollocks|bastard|idiot|arse|(holy ?|horse ?)?shit(show|hole)?|gods?damn|son ?of ?a ?(bitch|motherless ?goat|whore)|slut|twat', re.IGNORECASE)