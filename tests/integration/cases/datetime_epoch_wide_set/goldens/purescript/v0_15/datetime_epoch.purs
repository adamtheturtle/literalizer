module Check where


data Val
    = PInt Int
    | PLong Number
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PLong 4085195400.0
]
