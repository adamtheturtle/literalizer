module Check where


data Val
    = PNull
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PNull,
    PNull
    ]
