module Fixture_call_elm_bound_multiline_multiple_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
f :: Val -> IO ()
f _ = return ()
ref_data :: Val
ref_data = HList [
    1,
    2
    ]
main :: IO ()
main = do
    _ <- f (HList [
        ref_data
        ])
    _ <- f (HList [
        ref_data
        ])
    pure ()
