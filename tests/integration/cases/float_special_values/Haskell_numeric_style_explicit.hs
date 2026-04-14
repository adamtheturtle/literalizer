module Check where
data Val = HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HFloat ((1/0)),
    HFloat ((-1/0)),
    HFloat ((0/0))
    ]
