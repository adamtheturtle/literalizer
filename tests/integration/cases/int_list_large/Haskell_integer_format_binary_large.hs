module Check where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    0b11110100001001000000,
    -0b10011010010,
    0b11111111,
    -0b1010
    ]
