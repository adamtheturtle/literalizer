module Check where


data Val
    = PInt Int
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PInt 0x1,
    PInt 0x2,
    PInt 0x3
]
