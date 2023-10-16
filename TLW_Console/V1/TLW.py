import os
import secrets
import sys
import cv2
# import random

# cardPic = cv2.imread("Base_Card_Supersized_Back.png", cv2.IMREAD_ANYCOLOR)
EVENTCARD_PATH = "V1/CardImages/EventCards/"
CURRENCYCARD_PATH = "V1/CardImages/CoinCards/"

pic_Default = cv2.imread(EVENTCARD_PATH + "Base_Card_Supersized.png", cv2.IMREAD_ANYCOLOR)

pic_currencyPositive3 = cv2.imread(CURRENCYCARD_PATH + "coinCard_Plus3_Supersized.png", cv2.IMREAD_ANYCOLOR)
pic_currencyPositive2 = cv2.imread(CURRENCYCARD_PATH + "coinCard_Plus2_Supersized.png", cv2.IMREAD_ANYCOLOR)
pic_currencyNegative2 = cv2.imread(CURRENCYCARD_PATH + "coinCard_Minus2_Supersized.png", cv2.IMREAD_ANYCOLOR)
pic_currencyNegative1 = cv2.imread(CURRENCYCARD_PATH + "coinCard_Minus1_Supersized.png", cv2.IMREAD_ANYCOLOR)

# ------------------------------------------------------------
# Card Declarations
class Card:
    def __init__(self, name, areaOfEffect, durationText, lightText="No Effect", voidText="No Effect", hasPic=False, cardFront=pic_Default) -> None:
        self.name = name
        self.durationText = durationText
        self.areaOfEffect = areaOfEffect
        self.lightText = lightText
        self.voidText = voidText
        self.hasPic = hasPic
        self.cardFront = cardFront
    
    def PrintCard(self):
        print("----- " + self.name + " : " + self.areaOfEffect + " -----")
        print("--------------------")
        print(self.durationText)
        print("--------------------")
        print("----- Light -----")
        print(self.lightText)
        print("--------------------")
        print("----- Void -----")
        print(self.voidText)
        print("--------------------")
    
    def ShowCardPic(self):
        if(self.hasPic):
            print("Look at pic")
            WaitForEnter()
            while True:
                cv2.imshow(self.name, self.cardFront)
                # WaitForEnter()
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
# ------------------------------------------------------------

# ------------------------------------------------------------
# Declarations
# ----- Eventcards -----
card_Lightstorm = Card("Lightstorm", "Global", "Lasts 2 turns", "+1 life per turn\n+1 movement", "Half movement")
card_Voidstorm = Card("Voidstorm", "Global", "Lasts 2 turns", "-1 life per turn\n-2 movement", "Moving through the middle is free\nWatch tower can be activated remotely")
card_Energize = Card("Energize", "Quadrant", "Lasts 2 turns", "+2 Movement", "+2 Movement")
card_DeEnergize = Card("De-Energize", "Quadrant", "Lasts 2 turns", "-2 Movement", "-1 Movement")
card_Bandit = Card("Bandit", "Global", "1 Time event", "Richest player gives Poorest Player\nhalf their money if either of\nthose Players actived this event")
card_Invisible = Card("Invisibility", "Individual", "Lasts 2 turns", "Invisibility\n Untargetable", "True sight")
card_ArrowRain = Card("Arrow Rain", "Global", "1 Time event", "Each player rolls a D6\nUneven number means you loose 3 HP")
card_Rush = Card("Rush", "Quadrant", "Lasts 2 turns", "Players have to walk the full diceroll", "1 Player gets the effect [Roll D8] and count infront of you")
card_Blinding = Card("Blinding", "Voidmaster", "Lasts 1 turn", "Voidmaster has to move the full diceroll", "You have to move the full diceroll")
card_PortableShop = Card("Portable Shop", "Individual", "1 Time event", "Lets you buy anything from the shop", "Lets you buy anything from the shop")
card_Rewind = Card("Rewind", "Individual", "1 Time event", "[Roll a D6, Divide by 2] and walk backwards the amount", "Walk back 2 steps")
card_Replay = Card("Replay", "Individual", "1 Time event", "You get another turn", "You get another turn")
card_Shortcut = Card("Shortcut", "Individual", "1 Time event", "Move up to 5 steps forward or back", "Move up to 5 steps forward or back\nor TP into the watchtower")
card_FoundKey = Card("Key", "Individual", "1 Time event", "Found a key", "Destroy the key")

cardEventListDefault = [
    card_Lightstorm, card_Voidstorm, card_FoundKey, card_FoundKey, card_FoundKey,
    card_Energize, card_DeEnergize, card_Energize, card_DeEnergize,
    card_Bandit, card_Bandit,
    card_Invisible, card_Invisible,
    card_ArrowRain, card_ArrowRain,
    card_Rush, card_Rush, card_Blinding,
    card_PortableShop, card_PortableShop,
    card_Rewind, card_Rewind,
    card_Replay, card_Replay, card_Replay,
    card_Shortcut, card_Shortcut, card_Shortcut
]
gameDeck = cardEventListDefault
# ----- Eventcards -----

# ----- Currencycards -----
card_CurrencyPositive3 = Card("Coin & Mana", "Individual", "1 Time", "+3 Coins", "+3 Mana", True, pic_currencyPositive3)
card_CurrencyPositive2 = Card("Coin & Mana", "Individual", "1 Time", "+2 Coins", "+2 Mana", True, pic_currencyPositive2)
card_CurrencyNegative2 = Card("Coin & Mana", "Individual", "1 Time", "-2 Coins", "-2 Mana", True, pic_currencyNegative2)
card_CurrencyNegative1 = Card("Coin & Mana", "Individual", "1 Time", "-1 Coin", "-1 Mana", True, pic_currencyNegative1)

cardCurrencyListDefault = [
    card_CurrencyPositive3,
    card_CurrencyPositive3,
    card_CurrencyPositive2,
    card_CurrencyPositive2,
    card_CurrencyPositive2,
    card_CurrencyPositive2,

    card_CurrencyNegative2,
    card_CurrencyNegative1,
    card_CurrencyNegative1,
    card_CurrencyNegative1
    ]
currencyDeck = cardCurrencyListDefault
# ----- Coincards -----
# ------------------------------------------------------------

# ------------------------------------------------------------
# Functions
def WaitForEnter():
    print("Press enter to continue ")
    _ = input()

def GetPlayerInput(messageString):
    print(messageString)
    _pI = input()
    return _pI

def ClearConsole():
    os.system("cls")
# ------------------------------------------------------------

# ------------------------------------------------------------
# ------------------------------
# Game Loop
def GameLoop(_cardEventListDefalt, _gameDeck, _currencyDeck):
    ClearConsole()
    print("----------------------- NEW GAME -----------------------")
    isGameOver = True
    while(isGameOver):
        print("----------------------- The Light Within -----------------------")
        print("[E] - Eventcard")
        print("[C] - Coincard")
        print("[Q] - Quit")
        playerChoice = GetPlayerInput("What action do you wish to take?")

        if(playerChoice == "q" or playerChoice == "Q"):
            isGameOver = False

        elif(playerChoice == "e" or playerChoice == "E"):
            if(len(_gameDeck) == 0): # Fixa senare istället för omstart adda reschuffle
                # _gameDeck.clear()
                # _gameDeck = _cardEventListDefalt.copy()
                print("POG")
            elif(len(_gameDeck) == 1):
                _randNr = 0
            else:
                _randNr = secrets.randbelow(len(_gameDeck))
            
            if(len(_gameDeck) <= 0):
                print("ReSchuffle")
                WaitForEnter()
                isGameOver = True
            
            if(True): # Error when _gameDeck is empty
                _curCard = _gameDeck[_randNr]
                _gameDeck.pop(_randNr)
                _curCard.PrintCard()
                if _curCard.hasPic:
                    _curCard.ShowCardPic()
                    cv2.destroyAllWindows()
    
        elif(playerChoice == "c" or playerChoice == "C"):
            _randCurrencyCard = secrets.choice(_currencyDeck)
            _randCurrencyCard.PrintCard()
            if _randCurrencyCard.hasPic:
                _randCurrencyCard.ShowCardPic()
                cv2.destroyAllWindows()
    
        WaitForEnter()
        ClearConsole()
    WaitForEnter()
    
# ------------------------------
# ------------------------------------------------------------

# Start Game
if __name__ == "__main__":
    GameLoop(cardEventListDefault, gameDeck, currencyDeck)