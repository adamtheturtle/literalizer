{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_no_params_curried_dotted_Haskell_call where
data Val = HList [Val]
data ThrottlerType_ = ThrottlerType_ { check :: IO () }
throttler :: ThrottlerType_
throttler = ThrottlerType_ { check = return () }
main :: IO ()
main = do
    _ <- throttler.check
    _ <- throttler.check
    pure ()
