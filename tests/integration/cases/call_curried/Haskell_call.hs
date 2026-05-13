{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_curried_Haskell_call where
data Val = HFloat Double | HStr String | HList [Val]
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
data ThrottlerType_ = ThrottlerType_ { check :: Val -> Val -> IO Val }
throttler :: ThrottlerType_
throttler = ThrottlerType_ { check = \_ _ -> return undefined }
emit :: a -> IO ()
emit _ = return ()
main :: IO ()
main = do
    _ <- emit (throttler.check (HStr "user_1") (1000.0))
    _ <- emit (throttler.check (HStr "user_2") (2000.5))
    pure ()
