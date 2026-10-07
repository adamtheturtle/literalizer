module Check where


data Val
    = PInt Int
    | PFloat Number
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PFloat 2.5,
    PInt 1
]
