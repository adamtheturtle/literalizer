module Fixture_call_mixed_scalar_type_arguments_Haskell_datetime_iso_call where
import Data.Time (Day, fromGregorian)
data Val = HFloat Double | HStr String | HList [Val] | HDate Day
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
capture :: Val -> Val -> Val -> Val -> Val -> Val -> Val -> IO ()
capture _ _ _ _ _ _ _ = return ()
main :: IO ()
main = do
    _ <- capture (HFloat ((0/0))) (HFloat ((1/0))) (HFloat ((-1/0))) (1.25) (HDate (fromGregorian 2024 1 15)) (HStr "2024-01-15T12:34:56") (HStr "[ordinary text]")
    pure ()
