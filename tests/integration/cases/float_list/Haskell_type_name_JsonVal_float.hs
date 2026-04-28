module Fixture_float_list_Haskell_type_name_JsonVal_float where
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
    1.1,
    -2.2,
    3.3
    ]
main :: IO ()
main = seq my_data (return ())
