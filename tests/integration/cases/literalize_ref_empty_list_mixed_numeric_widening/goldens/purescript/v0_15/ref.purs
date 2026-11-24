module Check where


data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


emptyValues :: Val
emptyValues = PList []
integerValues :: Val
integerValues = PList [
    PInt 1
]
floatValues :: Val
floatValues = PList [
    PFloat 1.5
]
my_data :: Val
my_data = PList [
    emptyValues,
    integerValues,
    floatValues
]
