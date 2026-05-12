{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_homogeneous_dotted_method_Haskell_call where
data Val = HStr String | HList [Val]
data ClientType_ = ClientType_ { fetch :: Val -> IO () }
data AppType_ = AppType_ { client :: ClientType_ }
app :: AppType_
app = AppType_ { client = ClientType_ { fetch = \_ -> return () } }
main :: IO ()
main = do
    _ <- app.client.fetch(HStr "hello")
    _ <- app.client.fetch(HStr "world")
    pure ()
