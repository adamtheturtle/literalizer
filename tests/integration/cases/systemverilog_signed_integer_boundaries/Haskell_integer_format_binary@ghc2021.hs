{-# LANGUAGE BinaryLiterals #-}
module Fixture_systemverilog_signed_integer_boundaries_Haskell_integer_format_binary where
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
    ("i32_below", -0b10000000000000000000000000000001),
    ("i32_minimum", -0b10000000000000000000000000000000),
    ("i32_above", -0b1111111111111111111111111111111),
    ("i32_maximum", 0b1111111111111111111111111111111),
    ("i32_over", 0b10000000000000000000000000000000),
    ("i64_minimum", -0b1000000000000000000000000000000000000000000000000000000000000000),
    ("i64_maximum", 0b111111111111111111111111111111111111111111111111111111111111111)
    ]
main :: IO ()
main = seq my_data (return ())
