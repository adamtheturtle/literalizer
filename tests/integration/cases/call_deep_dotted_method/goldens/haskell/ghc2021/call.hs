{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_deep_dotted_method_Haskell_call where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data ClientType_ = ClientType_ { post :: Val -> IO () }
data ApiType_ = ApiType_ { client :: ClientType_ }
data ObjType_ = ObjType_ { api :: ApiType_ }
obj :: ObjType_
obj = ObjType_ { api = ApiType_ { client = ClientType_ { post = \_ -> return () } } }
main :: IO ()
main = do
    _ <- obj.api.client.post (HStr "hello")
    _ <- obj.api.client.post (42)
    _ <- obj.api.client.post (HBool True)
    pure ()
