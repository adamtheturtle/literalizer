module Check where


data Val
    = PInt Int
    | PList (Array Val)


refData :: Val
refData = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = refData
