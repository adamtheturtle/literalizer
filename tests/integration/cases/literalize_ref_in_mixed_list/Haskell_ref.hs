module Fixture_literalize_ref_in_mixed_list_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
x :: Val
x = HMap [
    ("_", HStr "_")
    ]
my_data :: Val
my_data = HList [
    x,
    1,
    2
    ]
main :: IO ()
main = seq my_data (return ())
