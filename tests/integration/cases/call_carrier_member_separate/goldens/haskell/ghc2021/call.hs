{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_carrier_member_separate_Haskell_call where
data AppType_ = AppType_ { go :: Val -> Val -> IO () }
app :: AppType_
app = AppType_ { go = \_ _ -> return () }
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
main :: IO ()
main = do
    _ <- app.go (HList [1]) (HList [HStr "text"])
    pure ()
