module Fixture_record_uniform_list_fields_Haskell where
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
my_data = HList [
    HMap [("scores", HList [1, 2])],
    HMap [("scores", HList [3, 4])]
    ]
main :: IO ()
main = seq my_data (return ())
