module Fixture_sibling_list_values_same_shape_Haskell_type_hints_safe where
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
    ("test", HList [5, HList [HStr "compile", HStr "test"]]),
    ("package", HList [7, HList [HStr "link", HStr "test"]])
    ]
main :: IO ()
main = seq my_data (return ())
