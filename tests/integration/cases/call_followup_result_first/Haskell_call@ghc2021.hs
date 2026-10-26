{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_followup_result_first_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
make_widget :: Val -> Val -> IO Val
make_widget _ _ = return undefined
consume :: (IO Val) -> Val -> IO ()
consume _ _ = return ()
my_data = make_widget (42) (3)
main :: IO ()
main = do
    _ <- consume my_data (3)
    pure ()
