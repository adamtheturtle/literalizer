{-# LANGUAGE OverloadedStrings #-}
module Check where
import Data.String (IsString(fromString))
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance IsString Val where
    fromString = HStr
instance Num Val where
    fromInteger = HInt
    a + b = error "not implemented"
    a * b = error "not implemented"
    abs a = error "not implemented"
    signum a = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
data ClientType_ = ClientType_ { post :: Val -> IO () }
data ApiType_ = ApiType_ { client :: ClientType_ }
data ObjType_ = ObjType_ { api :: ApiType_ }
obj = ObjType_ { api = ApiType_ { client = ClientType_ { post = \_ -> return () } } }
main :: IO ()
main = do
    (post (client (api obj)))("hello")
    (post (client (api obj)))(42)
    (post (client (api obj)))(HBool True)
    pure ()
