{-# LANGUAGE OverloadedRecordDot #-}
module Check where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data ApiType_ = ApiType_ { request :: Val -> IO () }
data ClientType_ = ClientType_ { api :: ApiType_ }
client = ClientType_ { api = ApiType_ { request = \_ -> return () } }
main :: IO ()
main = do
    client.api.request(HStr "hello")
    client.api.request(42)
    client.api.request(HBool True)
    pure ()
