module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "2024-01-15T12:30:00.123456+00:00",
    PStr "2024-06-01T08:00:00+00:00"
    ]
