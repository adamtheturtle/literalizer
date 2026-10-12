{-# LANGUAGE BinaryLiterals #-}
module Fixture_purescript_int32_minimum_Haskell_integer_format_binary where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
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
    ("neighbor", -0b1111111111111111111111111111111),
    ("maximum", 0b1111111111111111111111111111111),
    ("nested", HList [-0b10000000000000000000000000000000])
    ]
main :: IO ()
main = seq my_data (return ())
