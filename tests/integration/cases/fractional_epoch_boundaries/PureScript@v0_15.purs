module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "1970-01-01T00:00:00.000001+00:00",
    PStr "1969-12-31T23:59:59.500000+00:00",
    PStr "1970-01-01T00:00:01+00:00"
]
