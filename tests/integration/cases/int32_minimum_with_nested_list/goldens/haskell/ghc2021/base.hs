module Fixture_int32_minimum_with_nested_list_Haskell where
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
    ("minimum", -2147483648),
    ("neighbor", -2147483647),
    ("maximum", 2147483647),
    ("nested", HList [-2147483648])
    ]
main :: IO ()
main = seq my_data (return ())
