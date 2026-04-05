module Check where


data Val
    = PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PStr "apple",
    PStr "banana",
    PStr "cherry"
    ]
