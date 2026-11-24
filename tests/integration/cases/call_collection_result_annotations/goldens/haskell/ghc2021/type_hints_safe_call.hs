{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_collection_result_annotations_Haskell_type_hints_safe_call where
make_widget :: Val -> IO Val
make_widget _ = return undefined
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data = make_widget (HList [HList [1, 2], HList [3]])
main :: IO ()
main = seq my_data (return ())
