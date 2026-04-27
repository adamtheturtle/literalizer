module Fixture_float_special_values_Haskell_prefix_J_v where
data Val = JFloat Double | JList [Val]
instance Num Val where
    fromInteger n = JFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (JFloat f) = JFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = JFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = JList [
    (1/0),
    (-1/0),
    (0/0)
    ]
