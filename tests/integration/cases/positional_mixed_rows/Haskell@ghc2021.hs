module Fixture_positional_mixed_rows_Haskell where
data Val = HInt Integer | HStr String | HList [Val]
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
    HList [HList [1, HStr "value"], HList [1, 2], HList []],
    HList [HList [], HList [], HList [3, 4]]
    ]
main :: IO ()
main = seq my_data (return ())
