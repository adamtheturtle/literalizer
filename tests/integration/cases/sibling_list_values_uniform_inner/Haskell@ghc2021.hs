module Fixture_sibling_list_values_uniform_inner_Haskell where
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
    ("lint", HList [2, HList [1]]),
    ("test", HList [5, HList [7]])
    ]
main :: IO ()
main = seq my_data (return ())
