module Check where
data Val = HFloat Double | HList [Val]
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    a / b = error "not implemented"
my_data :: Val
my_data = HList [
    HList [1.500000, 2.500000],
    HList [3.500000, 4.500000]
    ]
