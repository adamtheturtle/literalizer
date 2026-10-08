{-# LANGUAGE BinaryLiterals #-}
module Fixture_nim_non_decimal_i64_min_Haskell_integer_format_binary where
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
    -0b1000000000000000000000000000000000000000000000000000000000000000,
    -0b1,
    0b111111111111111111111111111111111111111111111111111111111111111
    ]
main :: IO ()
main = seq my_data (return ())
