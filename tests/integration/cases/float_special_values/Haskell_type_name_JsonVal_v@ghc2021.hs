module Fixture_float_special_values_Haskell_type_name_JsonVal_v where
data JsonVal = HFloat Double | HList [JsonVal]
instance Num JsonVal where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional JsonVal where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: JsonVal
my_data = HList [
    (1/0),
    (-1/0),
    (0/0)
    ]
main :: IO ()
main = seq my_data (return ())
