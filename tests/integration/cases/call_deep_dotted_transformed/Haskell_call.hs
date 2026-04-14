{-# LANGUAGE OverloadedStrings #-}
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
data ClientType_ = ClientType_ { fetch :: () -> () }
data AppType_ = AppType_ { client :: ClientType_ }
app = AppType_ { client = ClientType_ { fetch = const () } }
emit _ = ()
emit(app.client.fetch("hello"))
emit(app.client.fetch(42))
emit(app.client.fetch(HBool True))
