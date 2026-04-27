module Check where
data Val = HInt Integer | HList [Val]
my_data :: Val
my_data = HList [
    HInt 1,
    HInt 2,
    HInt 3
    ]
