module Check where


data Val
    = PInt Int
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PInt 10,  -- comment for ten
    PInt 2  -- comment for two
]
