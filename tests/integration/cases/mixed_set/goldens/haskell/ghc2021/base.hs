module Fixture_mixed_set_Haskell where
data Val = HBool Bool | HInt Integer | HStr String | HSet [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HSet [
    HBool True,
    42,
    HStr "apple"
    ]
main :: IO ()
main = seq my_data (return ())
