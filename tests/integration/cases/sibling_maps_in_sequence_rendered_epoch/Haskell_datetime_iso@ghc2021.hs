module Fixture_sibling_maps_in_sequence_rendered_epoch_Haskell_datetime_iso where
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
    HMap [("k", HStr "2040-01-01T00:00:00+00:00")],
    HMap [("k", 1)]
    ]
main :: IO ()
main = seq my_data (return ())
