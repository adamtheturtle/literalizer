module Check where
data Val = HBool Bool | HInt Integer | HStr String | HSet [Val]
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HSet [
    HBool True,
    42,
    HStr "apple"
    ]
