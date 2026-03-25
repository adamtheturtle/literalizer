module Check where
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)] | HSet [Val]
my_data :: Val
my_data = HList [
    HList [],
    HList []
]
