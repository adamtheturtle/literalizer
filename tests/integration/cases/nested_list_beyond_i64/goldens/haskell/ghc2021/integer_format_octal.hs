module Fixture_nested_list_beyond_i64_Haskell_integer_format_octal where
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
    HList [0o1],
    HList [0o200000000000000000000000]
    ]
main :: IO ()
main = seq my_data (return ())
