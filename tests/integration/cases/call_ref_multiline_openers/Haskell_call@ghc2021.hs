module Fixture_call_ref_multiline_openers_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
consume :: Val -> Val -> IO ()
consume _ _ = return ()
foo :: Val
foo = 42
main :: IO ()
main = do
    _ <- consume (HList [
    _ <-     HMap [
    _ <-         ("other", 1)
    _ <-         ],
    _ <-     foo
    _ <-     ]) (HMap [
    _ <-     ("left", foo),
    _ <-     ("other", 1)
    _ <-     ])
    pure ()
