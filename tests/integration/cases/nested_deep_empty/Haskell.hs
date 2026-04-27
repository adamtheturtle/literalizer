module check where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [HList [], HList []]
    ]
