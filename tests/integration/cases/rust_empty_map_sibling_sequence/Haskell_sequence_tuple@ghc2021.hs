module Fixture_rust_empty_map_sibling_sequence_Haskell_sequence_tuple where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: (Val, Val)
my_data = (
    HMap [("a", 1)],
    HMap []
    )
main :: IO ()
main = seq my_data (return ())
