module Fixture_roc_call_alias_discarded_Haskell_type_name_JsonVal_call where
data JsonVal = HInt Integer
instance Num JsonVal where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
process :: JsonVal -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process (1)
    pure ()
