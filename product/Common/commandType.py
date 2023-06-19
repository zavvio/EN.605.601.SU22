from enum import Enum


class CommandType(Enum):
    # From Client to Server
    cmdInit = 1
    cmdKeepAlive = 2
    cmdSpinWheel = 3
    cmdAnswer = 4
    cmdRequestScore = 5
    cmdReady = 6
    cmdPickCategory = 7
    cmdUseToken = 8

    # From Server to Client
    cmdQuestion = 101
    cmdDeliveryScore = 102
    cmdQuestionSet = 103
    cmdStatusPacket = 104
