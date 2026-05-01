module Fixture_call_per_element_false_dict_arg_Haskell_call where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
send :: Val -> IO ()
send _ = return ()
main :: IO ()
main = do
    _ <- send(HMap [("a", 1), ("b", HStr "x")])
    pure ()
