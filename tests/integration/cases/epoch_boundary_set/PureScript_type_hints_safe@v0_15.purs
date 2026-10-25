module Check where


data Val
    = PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PStr "1901-12-13T20:45:51",
    PStr "1901-12-13T20:45:52",
    PStr "2038-01-19T03:14:07",
    PStr "2038-01-19T03:14:08"
]
