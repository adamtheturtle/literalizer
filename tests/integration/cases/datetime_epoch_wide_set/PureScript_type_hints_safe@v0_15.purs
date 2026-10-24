module Check where


data Val
    = PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PStr "2099-06-15T08:30:00"
]
