module Fixture_call_mixed_scalar_type_arguments_Haskell_datetime_epoch_call where
import Data.Time (Day, fromGregorian)
data Val = HFloat Double | HStr String | HList [Val] | HDate Day | HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
capture :: Val -> Val -> Val -> Val -> Val -> Val -> Val -> IO ()
capture _ _ _ _ _ _ _ = return ()
main :: IO ()
main = do
    _ <- capture (HFloat ((0/0))) (HFloat ((1/0))) (HFloat ((-1/0))) (1.25) (HDate (fromGregorian 2024 1 15)) (1705322096) (HStr "[ordinary text]")
    pure ()
