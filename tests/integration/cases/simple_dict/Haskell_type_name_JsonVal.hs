module Check where
data JsonVal = HNull | HBool Bool | HInt Integer | HStr String | HMap [(String, JsonVal)]
instance Num JsonVal where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: JsonVal
my_data = HMap [
    ("name", HStr "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", HNull)
    ]
