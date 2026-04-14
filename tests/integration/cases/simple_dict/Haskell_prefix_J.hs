module Check where
data Val = JNull | JBool Bool | JInt Integer | JStr String | JMap [(String, Val)]
instance Num Val where
    fromInteger = JInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (JInt n) = JInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = JMap [
    ("name", JStr "Alice"),
    ("age", 30),
    ("active", JBool True),
    ("score", JNull)
    ]
