module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "100% done",
    PStr "%(name) is here"
    ]
