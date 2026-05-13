{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_snake_dotted_method_Haskell_call where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data Http_clientType_ = Http_clientType_ { fetch :: Val -> IO () }
data My_appType_ = My_appType_ { http_client :: Http_clientType_ }
my_app :: My_appType_
my_app = My_appType_ { http_client = Http_clientType_ { fetch = \_ -> return () } }
main :: IO ()
main = do
    _ <- my_app.http_client.fetch (HStr "hello")
    _ <- my_app.http_client.fetch (42)
    _ <- my_app.http_client.fetch (HBool True)
    pure ()
