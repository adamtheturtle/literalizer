module Check where
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HInt 42,
    HFloat (3.14),
    HBool True,
    HBool False,
    HStr "hello \"world\""
    ]
