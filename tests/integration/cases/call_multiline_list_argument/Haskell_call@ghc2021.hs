module Fixture_call_multiline_list_argument_Haskell_call where
process :: Val -> IO ()
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
    _ <- process (HList [
    _ <-     1,
    _ <-     2
    _ <-     ])
    _ <- process (HList [
    _ <-     3
    _ <-     ])
    pure ()
