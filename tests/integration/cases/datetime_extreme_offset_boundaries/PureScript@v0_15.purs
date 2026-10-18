module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "2020-06-15T12:00:00-23:59",
    PStr "2020-06-15T12:00:00-18:00",
    PStr "2020-06-15T12:00:00+18:00",
    PStr "2020-06-15T12:00:00+23:59"
]
