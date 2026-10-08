module Fixture_go_widened_dict_elements_Haskell where
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
    ("a", HList [HMap [], HMap [("x", 1)]]),
    ("b", HList [HList [], HList [1]])
    ]
main :: IO ()
main = seq my_data (return ())
