{-# LANGUAGE BinaryLiterals #-}
module Fixture_cpp_variant_int32_boundaries_sequence_Haskell_integer_format_binary where
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
    -0b10000000000000000000000000000000,
    -0b1111111111111111111111111111111,
    HList [0b0]
    ]
main :: IO ()
main = seq my_data (return ())
