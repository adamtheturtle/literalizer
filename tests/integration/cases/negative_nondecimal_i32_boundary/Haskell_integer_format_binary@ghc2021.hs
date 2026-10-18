{-# LANGUAGE BinaryLiterals #-}
module Fixture_negative_nondecimal_i32_boundary_Haskell_integer_format_binary where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("minimum", -0b10000000000000000000000000000000),
    ("below", -0b10110010110100000101111000000000)
    ]
main :: IO ()
main = seq my_data (return ())
