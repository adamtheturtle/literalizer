module Check where
data Val = JFloat Double | JList [Val]
instance Num Val where
    fromInteger n = JFloat (fromIntegral n)
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (JFloat f) = JFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = JFloat (realToFrac r)
    a / b = error "not implemented"
my_data :: Val
my_data = JList [
    1.1,
    -2.2,
    3.3
    ]
