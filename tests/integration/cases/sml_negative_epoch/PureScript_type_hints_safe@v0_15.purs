module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "1960-01-01T00:00:00+00:00"
]
