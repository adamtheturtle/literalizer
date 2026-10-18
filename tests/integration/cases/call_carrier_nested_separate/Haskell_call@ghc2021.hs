{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_carrier_nested_separate_Haskell_call where
data ClientType_ = ClientType_ { go :: Val -> Val -> IO () }
data AppType_ = AppType_ { client :: ClientType_ }
app :: AppType_
app = AppType_ { client = ClientType_ { go = \_ _ -> return () } }
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
    _ <- app.client.go (HList [1]) (HList [HStr "text"])
    pure ()
