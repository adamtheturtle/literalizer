module Check where


data Val
    = PInt Int
    | PList (Array Val)


emptyValues :: Val
emptyValues = PList []
integerValues :: Val
integerValues = PList [
    PInt 1
]
my_data :: Val
my_data = PList [
    emptyValues,
    integerValues
]
