import json
import requests
import tempfile
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

tabletop_sim_deck_code = '''{"ObjectStates":[{"Name":"DeckCustom","ContainedObjects":[{"CardID":100,"Name":"Card","Nickname":"Yzma - Scary Beyond All Reason","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":100,"Name":"Card","Nickname":"Yzma - Scary Beyond All Reason","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":100,"Name":"Card","Nickname":"Yzma - Scary Beyond All Reason","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":100,"Name":"Card","Nickname":"Yzma - Scary Beyond All Reason","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":504,"Name":"Card","Nickname":"Fire The Cannons!","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":504,"Name":"Card","Nickname":"Fire The Cannons!","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":706,"Name":"Card","Nickname":"Friends On The Other Side","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":706,"Name":"Card","Nickname":"Friends On The Other Side","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":706,"Name":"Card","Nickname":"Friends On The Other Side","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1009,"Name":"Card","Nickname":"Captain Hook - Forceful Duelist","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1009,"Name":"Card","Nickname":"Captain Hook - Forceful Duelist","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1009,"Name":"Card","Nickname":"Captain Hook - Forceful Duelist","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1009,"Name":"Card","Nickname":"Captain Hook - Forceful Duelist","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1413,"Name":"Card","Nickname":"A Whole New World","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1413,"Name":"Card","Nickname":"A Whole New World","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1413,"Name":"Card","Nickname":"A Whole New World","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1413,"Name":"Card","Nickname":"A Whole New World","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1817,"Name":"Card","Nickname":"Tinker Bell - Tiny Tactician","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1817,"Name":"Card","Nickname":"Tinker Bell - Tiny Tactician","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1817,"Name":"Card","Nickname":"Tinker Bell - Tiny Tactician","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":1817,"Name":"Card","Nickname":"Tinker Bell - Tiny Tactician","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2221,"Name":"Card","Nickname":"Magic Broom - Bucket Brigade","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2221,"Name":"Card","Nickname":"Magic Broom - Bucket Brigade","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2221,"Name":"Card","Nickname":"Magic Broom - Bucket Brigade","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2524,"Name":"Card","Nickname":"Smash","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2524,"Name":"Card","Nickname":"Smash","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2524,"Name":"Card","Nickname":"Smash","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2524,"Name":"Card","Nickname":"Smash","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":2928,"Name":"Card","Nickname":"Ursulas Cauldron","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3029,"Name":"Card","Nickname":"Grab Your Sword","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3029,"Name":"Card","Nickname":"Grab Your Sword","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3029,"Name":"Card","Nickname":"Grab Your Sword","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3029,"Name":"Card","Nickname":"Grab Your Sword","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3433,"Name":"Card","Nickname":"Madam Mim - Rival of Merlin","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3534,"Name":"Card","Nickname":"Madam Mim - Snake","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3534,"Name":"Card","Nickname":"Madam Mim - Snake","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3534,"Name":"Card","Nickname":"Madam Mim - Snake","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3837,"Name":"Card","Nickname":"Tinker Bell - Giant Fairy","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3837,"Name":"Card","Nickname":"Tinker Bell - Giant Fairy","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3837,"Name":"Card","Nickname":"Tinker Bell - Giant Fairy","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":3837,"Name":"Card","Nickname":"Tinker Bell - Giant Fairy","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4241,"Name":"Card","Nickname":"Yzma - Without Beauty Sleep","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4241,"Name":"Card","Nickname":"Yzma - Without Beauty Sleep","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4241,"Name":"Card","Nickname":"Yzma - Without Beauty Sleep","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4241,"Name":"Card","Nickname":"Yzma - Without Beauty Sleep","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4645,"Name":"Card","Nickname":"Beast - Forbidding Recluse","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4645,"Name":"Card","Nickname":"Beast - Forbidding Recluse","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4847,"Name":"Card","Nickname":"Benja - Guardian of the Dragon Gem","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4847,"Name":"Card","Nickname":"Benja - Guardian of the Dragon Gem","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4847,"Name":"Card","Nickname":"Benja - Guardian of the Dragon Gem","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":4847,"Name":"Card","Nickname":"Benja - Guardian of the Dragon Gem","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5251,"Name":"Card","Nickname":"Merlin - Rabbit","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5251,"Name":"Card","Nickname":"Merlin - Rabbit","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5251,"Name":"Card","Nickname":"Merlin - Rabbit","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5554,"Name":"Card","Nickname":"Beast - Tragic Hero","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5554,"Name":"Card","Nickname":"Beast - Tragic Hero","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5554,"Name":"Card","Nickname":"Beast - Tragic Hero","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5857,"Name":"Card","Nickname":"Madam Mim - Fox","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5857,"Name":"Card","Nickname":"Madam Mim - Fox","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}},{"CardID":5857,"Name":"Card","Nickname":"Madam Mim - Fox","Transform":{"posX":0,"posY":0,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}}],"DeckIDs":[100,201,302,403,504,605,706,807,908,1009,1110,1211,1312,1413,1514,1615,1716,1817,1918,2019,2120,2221,2322,2423,2524,2625,2726,2827,2928,3029,3130,3231,3332,3433,3534,3635,3736,3837,3938,4039,4140,4241,4342,4443,4544,4645,4746,4847,4948,5049,5150,5251,5352,5453,5554,5655,5756,5857,5958,6059],"CustomDeck":{"1":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-060_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"2":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-060_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"3":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-060_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"4":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-060_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"5":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-197_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"6":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-197_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"7":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-064_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"8":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-064_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"9":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-064_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"10":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"11":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"12":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"13":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"14":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-195_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"15":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-195_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"16":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-195_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"17":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-195_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"18":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-194_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"19":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-194_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"20":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-194_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"21":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-194_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"22":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-047_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"23":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-047_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"24":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-047_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"25":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-200_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"26":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-200_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"27":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-200_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"28":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-200_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"29":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-067_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"30":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-198_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"31":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-198_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"32":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-198_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"33":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-198_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"34":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-048_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"35":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-049_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"36":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-049_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"37":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-049_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"38":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-193_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"39":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-193_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"40":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-193_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"41":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/001-193_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"42":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-061_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"43":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-061_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"44":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-061_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"45":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-061_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"46":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-171_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"47":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-171_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"48":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"49":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"50":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"51":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-174_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"52":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-052_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"53":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-052_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"54":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-052_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"55":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-173_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"56":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-173_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"57":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-173_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"58":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-046_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"59":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-046_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true},"60":{"FaceURL":"https://images.dreamborn.ink/cards/en/tts/002-046_716x1000.jpeg","BackURL":"https://dreamborn.ink/images/cardback.png","NumHeight":1,"NumWidth":1,"BackIsHidden":true}},"Transform":{"posX":0,"posY":1,"posZ":0,"rotX":0,"rotY":180,"rotZ":180,"scaleX":2.5,"scaleY":1,"scaleZ":2.5}}]}'''

data = json.loads(tabletop_sim_deck_code)

data = data["ObjectStates"][0]

def download_image(url, image_cache):
    if url in image_cache:
        return image_cache[url]

    response = requests.get(url)
    if response.status_code == 200:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(response.content)
        temp_file.close()
        image_cache[url] = temp_file.name
        return temp_file.name
    return None

pdf_file = "lorcana_deck_2.pdf"
page_width, page_height = letter
landscape_letter = (page_height, page_width)
c = canvas.Canvas(pdf_file, pagesize=landscape_letter)

card_width, card_height = 2.5 * inch, 3.5 * inch
margin_x, margin_y = 0.5 * inch, 0.5 * inch

cards_per_row = int((landscape_letter[0] - 2 * margin_x) / card_width)
cards_per_column = int((landscape_letter[1] - 2 * margin_y) / card_height)

print(int((page_height - 2 * margin_x) / card_width) * int((page_width - 2 * margin_y) / card_height))

image_cache = {}

current_row = current_column = 0
for deck_id, deck_info in data["CustomDeck"].items():
    face_url = deck_info["FaceURL"]
    image = download_image(face_url, image_cache)
    if image:
        x = margin_x + current_column * card_width
        y = landscape_letter[1] - margin_y - card_height - (current_row * card_height)
        c.drawImage(image, x, y, width=card_width, height=card_height)
        
        current_column += 1
        if current_column >= cards_per_row:
            current_column = 0
            current_row += 1
            if current_row >= cards_per_column:
                c.showPage()
                current_row = 0

c.save()

for temp_file in image_cache.values():
    os.remove(temp_file)

print(f"PDF file '{pdf_file}' has been created with the card images.")