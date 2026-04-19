module Check where
data Val = HFloat Double | HStr String | HList [Val]
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
data ThrottlerType_ = ThrottlerType_ { check :: (Val, Val) -> IO () }
throttler = ThrottlerType_ { check = \_ -> return () }
emit _ = return ()
main :: IO ()
main = do
    emit(throttler.check(HStr "user_1", 1000.0))
    emit(throttler.check(HStr "user_2", 2000.5))
    pure ()
