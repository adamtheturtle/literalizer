{-# LANGUAGE OverloadedStrings #-}
{-# OPTIONS_GHC -fdefer-type-errors #-}
{-# LANGUAGE OverloadedRecordDot #-}
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
data ClientType_ = ClientType_ { post :: () -> IO () }
data ApiType_ = ApiType_ { client :: ClientType_ }
data ObjType_ = ObjType_ { api :: ApiType_ }
obj = ObjType_ { api = ApiType_ { client = ClientType_ { post = \_ -> return () } } }
main :: IO ()
main = do
    obj.api.client.post("hello")
    obj.api.client.post(42)
    obj.api.client.post(HBool True)
    pure ()
