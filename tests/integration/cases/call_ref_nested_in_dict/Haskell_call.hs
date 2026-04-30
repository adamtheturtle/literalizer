module Fixture_call_ref_nested_in_dict_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> IO ()
process _ = return ()
my_var :: Val
my_var = 42
main :: IO ()
main = do
    _ <- process(HMap [("key", my_var), ("count", 42)])
    pure ()
