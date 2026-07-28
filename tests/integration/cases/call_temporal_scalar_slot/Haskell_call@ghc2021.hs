module Fixture_call_temporal_scalar_slot_Haskell_call where
import Data.Time (UTCTime(..), fromGregorian, secondsToDiffTime)
data Val = HInt Integer | HList [Val] | HDatetime UTCTime | HStr String
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process (HStr "09:30:00")
    _ <- process (HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 0)))
    _ <- process (1)
    pure ()
