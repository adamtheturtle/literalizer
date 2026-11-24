module Check where


data Val
    = PNull
    | PInt Int
    | PList (Array Val)


myValue :: Val
myValue = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = myValue
