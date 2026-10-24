module Check where


data Val
    = PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PStr "1969-12-31T23:59:59+00:00"
]
