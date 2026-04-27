module Fixture_call_wrap_in_file_Haskell_call where
process :: (Val, Val) -> IO ()
process _ = return ()
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
main :: IO ()
main = do
    _ <- process(1, 2)
    _ <- process(3, 4)
    pure ()
