module Fixture_call_ref_only_mapping_values_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
consume :: Val -> IO ()
consume _ = return ()
item :: Val
item = 42
main :: IO ()
main = do
    _ <- consume (HMap [("field", item)])
    pure ()
