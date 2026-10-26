module Check where


data Val
    = PInt Int
    | PList (Array Val)


seed :: Val
seed = PInt 1
my_data :: Val
my_data = PList [
    PList [],
    PList [PList []],
    seed
]
