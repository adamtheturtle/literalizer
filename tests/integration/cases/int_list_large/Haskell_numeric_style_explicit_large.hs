module Check where
data Val = HInt Integer | HList [Val]
my_data :: Val
my_data = HList [
    HInt 1000000,
    HInt (-1234),
    HInt 255,
    HInt (-10)
    ]
