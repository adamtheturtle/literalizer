module Fixture_sibling_list_values_nested_Haskell where
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
    ("lint", HList [2, HList []]),
    ("test", HList [5, HList [HStr "compile"]])
    ]
main :: IO ()
main = seq my_data (return ())
