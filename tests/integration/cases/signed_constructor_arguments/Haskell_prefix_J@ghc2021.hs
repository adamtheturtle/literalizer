module Fixture_signed_constructor_arguments_Haskell_prefix_J where
data Val = JInt Integer | JFloat Double | JList [Val]
instance Num Val where
    fromInteger = JInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (JInt n) = JInt (negate n)
    negate (JFloat f) = JFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = JFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = JList [
    -42,
    0,
    42,
    -1.25,
    0.0,
    1.25
    ]
main :: IO ()
main = seq my_data (return ())
