module Check where


data Val
    = PNull
    | PList (Array Val)


myNull :: Val
myNull = PNull
my_data :: Val
my_data = PList [
    myNull,
    PNull
]
