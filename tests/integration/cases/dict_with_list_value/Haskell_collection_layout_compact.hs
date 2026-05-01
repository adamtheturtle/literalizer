module Fixture_dict_with_list_value_Haskell_collection_layout_compact where
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
    ("name", HStr "Alice"),
    ("scores", HList [10, 20, 30])
    ]
main :: IO ()
main = seq my_data (return ())
