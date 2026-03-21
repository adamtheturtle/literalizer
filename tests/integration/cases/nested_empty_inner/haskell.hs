module Check where
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]
x :: Val
x = HList [
    HList [],
    HList []
    ]
