module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


one :: Val
one = PInt 1
two :: Val
two = PStr "s"
my_data :: Val
my_data = PList [
    one,
    two
]
