module Fixture_literalize_ref_escaped_nested_dict_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
existing :: Val
existing = 1
my_data :: Val
my_data = HMap [
    ("nested", HList [0, existing])
    ]
main :: IO ()
main = seq my_data (return ())
