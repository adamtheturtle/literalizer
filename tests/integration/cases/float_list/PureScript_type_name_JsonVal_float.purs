module Check where


import Prelude
data JsonVal
    = PFloat Number
    | PList (Array JsonVal)


my_data :: JsonVal
my_data = PList [
    PFloat 1.1,
    PFloat (-2.2),
    PFloat 3.3
    ]
