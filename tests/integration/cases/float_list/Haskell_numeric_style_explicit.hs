module check where
data Val = HFloat Double | HList [Val]
my_data :: Val
my_data = HList [
    HFloat (1.1),
    HFloat (-2.2),
    HFloat (3.3)
    ]
