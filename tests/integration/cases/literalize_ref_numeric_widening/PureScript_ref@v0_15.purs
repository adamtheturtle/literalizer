module Check where


data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


floatingValue :: Val
floatingValue = PFloat 1.5
integerValue :: Val
integerValue = PFloat 2.0
my_data :: Val
my_data = PList [
    floatingValue,
    integerValue
]
