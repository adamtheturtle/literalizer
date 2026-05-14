{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_deep_dotted_transformed_Haskell_call where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data ClientType_ = ClientType_ { fetch :: Val -> IO Val }
data AppType_ = AppType_ { client :: ClientType_ }
app :: AppType_
app = AppType_ { client = ClientType_ { fetch = \_ -> return undefined } }
emit :: a -> IO ()
emit _ = return ()
main :: IO ()
main = do
    _ <- emit (app.client.fetch (HStr "hello"))
    _ <- emit (app.client.fetch (42))
    _ <- emit (app.client.fetch (HBool True))
    pure ()
