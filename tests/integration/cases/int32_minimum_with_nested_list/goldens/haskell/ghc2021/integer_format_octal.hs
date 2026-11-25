module Fixture_int32_minimum_with_nested_list_Haskell_integer_format_octal where
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
    ("minimum", -0o20000000000),
    ("neighbor", -0o17777777777),
    ("maximum", 0o17777777777),
    ("nested", HList [-0o20000000000])
    ]
main :: IO ()
main = seq my_data (return ())
