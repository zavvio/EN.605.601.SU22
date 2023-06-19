from enum import Enum


class UserStatus(Enum):
    # ##### Server-side Status #####
    usIdle = 1
    # usInGame = 2
    usSpin = 3
    usAnswer = 4
    usReady = 5
    usPickCategory = 6
    usUseToken = 7

    # ##### Client-side Status #####
    psUnknown = 100
    psIdle = 101
    psWait = 102
    psSpin = 103
    psShowQuestion = 104
    psPlayerChoice = 105
    psOpponentChoice = 106
    psGameOver = 107
    psSpinAgain = 108
    psCheckToken = 109

    # ##### Game Action #####
    gaNothing = 201
    gaSpin = 202
    gaAnswer = 203
    gaPlayerChoice = 204
    gaOpponentChoice = 205
    gaCategoryCompleted = 206
    gaSpinAgain = 207
    gaBankrupt = 208
    gaFreeTurn = 209
    gaCheckToken = 210
