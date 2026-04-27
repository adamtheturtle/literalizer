module check where
data Val = HInt Integer | HList [Val]
my_data :: Val
my_data = HList [
    HInt 0,
    HInt 1,
    HInt (-1)
    ]
