module Fixture_rectangular_map_sequence_shapes_Haskell_type_hints_safe where
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
    ("a", HList [HMap [("item", HList [1])]]),
    ("b", HList [HMap [("item", HList [2])]])
    ]
main :: IO ()
main = seq my_data (return ())
