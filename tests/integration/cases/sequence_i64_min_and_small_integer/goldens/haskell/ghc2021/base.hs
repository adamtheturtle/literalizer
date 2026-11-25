module Fixture_sequence_i64_min_and_small_integer_Haskell where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    -9223372036854775808,
    1
    ]
main :: IO ()
main = seq my_data (return ())
