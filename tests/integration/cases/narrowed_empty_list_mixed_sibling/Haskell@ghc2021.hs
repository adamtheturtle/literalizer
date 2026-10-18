module Fixture_narrowed_empty_list_mixed_sibling_Haskell where
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
    HList [1, HStr "two"],
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
