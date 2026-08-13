module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "]",
    PStr "a]",
    PStr "a]=",
    PStr "a]b"
    ]
