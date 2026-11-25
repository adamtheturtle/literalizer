module Check where


data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


integerValue :: Val
integerValue = PFloat 1.0
my_data :: Val
my_data = PList [
    integerValue,
    PFloat 1.5
]
