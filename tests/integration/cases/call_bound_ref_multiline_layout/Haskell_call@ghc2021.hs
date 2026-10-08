module Fixture_call_bound_ref_multiline_layout_Haskell_call where
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
x :: Val
x = HList [
    HList [
        1,
        2
        ],
    HList [
        3,
        4
        ]
    ]
main :: IO ()
main = do
    _ <- f (HList [
        HList [
            x
            ]
        ])
    pure ()
