module Check where
data Val = HNull | HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data = (
    1,
    HStr "hello",
    HBool True,
    HNull
    )
