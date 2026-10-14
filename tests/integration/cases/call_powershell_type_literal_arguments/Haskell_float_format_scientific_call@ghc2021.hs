module Fixture_call_powershell_type_literal_arguments_Haskell_float_format_scientific_call where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
data Val = HFloat Double | HStr String | HList [Val] | HDate Day | HDatetime UTCTime
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
    _ <- capture ((0/0)) ((1/0)) ((-1/0)) (1.25) (HDate (fromGregorian 2024 1 15)) (HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 45296))) (HStr "[ordinary text]")
    pure ()
