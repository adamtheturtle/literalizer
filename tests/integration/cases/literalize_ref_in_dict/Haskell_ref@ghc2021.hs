module Fixture_literalize_ref_in_dict_Haskell_ref where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
myVar :: Val
myVar = 1
my_data :: Val
my_data = HMap [
    ("key", myVar)
    ]
main :: IO ()
main = seq my_data (return ())
