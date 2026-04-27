module Check where


data Val
    = PBool Boolean
    | PInt Int
    | PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PBool true,
    PInt 42,
    PStr "apple"
    ]
