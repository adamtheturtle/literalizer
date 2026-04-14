{-# LANGUAGE OverloadedStrings #-}
{-# OPTIONS_GHC -fdefer-type-errors #-}
{-# LANGUAGE OverloadedRecordDot #-}
module Check where
import Data.String (IsString(fromString))
data Val = HFloat Double | HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    a / b = error "not implemented"
data ThrottlerType_ = ThrottlerType_ { check :: () -> IO () }
throttler = ThrottlerType_ { check = \_ -> return () }
emit _ = return ()
main :: IO ()
main = do
    emit(throttler.check("user_1", 1000.0))
    emit(throttler.check("user_2", 2000.5))
    pure ()
