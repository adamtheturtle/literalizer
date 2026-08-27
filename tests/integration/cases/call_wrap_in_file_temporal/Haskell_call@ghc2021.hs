module Fixture_call_wrap_in_file_temporal_Haskell_call where
import Data.Time (Day, fromGregorian, UTCTime(..), secondsToDiffTime)
check :: Val -> Val -> IO ()
check _ _ = return ()
data Val = HList [Val] | HDate Day | HDatetime UTCTime
main :: IO ()
main = do
    _ <- check (HDatetime (UTCTime (fromGregorian 2024 1 15) (secondsToDiffTime 37800))) (HDate (fromGregorian 2024 6 1))
    pure ()
