{-# LANGUAGE BinaryLiterals #-}
module Fixture_tuple_top_level_Haskell_integer_format_binary where
data Val = HInt Integer | HStr String | HList [Val]
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
    0b1,
    HStr "email",
    HStr "a@gmail.com",
    0b1100100
    ]
main :: IO ()
main = seq my_data (return ())
