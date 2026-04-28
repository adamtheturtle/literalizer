module Fixture_int_list_large_Haskell_integer_format_octal_large where
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
    0o3641100,
    -0o2322,
    0o377,
    -0o12
    ]
main :: IO ()
main = seq my_data (return ())
