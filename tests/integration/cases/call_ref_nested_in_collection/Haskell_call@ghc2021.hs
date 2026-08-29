module Fixture_call_ref_nested_in_collection_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> Val -> IO ()
process _ _ = return ()
big_list :: Val
big_list = HList [
    HStr "x"
    ]
main :: IO ()
main = do
    _ <- process (HMap [("k", big_list)]) (2)
    pure ()
