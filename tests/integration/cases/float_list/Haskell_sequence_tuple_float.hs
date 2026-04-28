module Fixture_float_list_Haskell_sequence_tuple_float where
data Val = HFloat Double | HList [Val]
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: (Val, Val, Val)
my_data = (
    1.1,
    -2.2,
    3.3
    )
