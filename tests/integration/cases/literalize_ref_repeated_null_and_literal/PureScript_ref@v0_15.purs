module Check where


data Val
    = PNull
    | PList (Array Val)


value :: Val
value = PNull
my_data :: Val
my_data = PList [
    value,
    value,
    PNull
]
