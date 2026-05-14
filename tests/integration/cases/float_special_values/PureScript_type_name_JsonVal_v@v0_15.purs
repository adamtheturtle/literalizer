module Check where


import Prelude
data JsonVal
    = PFloat Number
    | PList (Array JsonVal)


my_data :: JsonVal
my_data = PList [
    PFloat (1.0 / 0.0),
    PFloat (-(1.0 / 0.0)),
    PFloat (0.0 / 0.0)
    ]
