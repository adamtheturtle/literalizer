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
data ClientType_ = ClientType_ { fetch :: Val -> IO () }
data AppType_ = AppType_ { client :: ClientType_ }
app = AppType_ { client = ClientType_ { fetch = \_ -> return () } }
main :: IO ()
main = do
    (fetch (client app))(HStr "hello")
    (fetch (client app))(42)
    (fetch (client app))(HBool True)
    pure ()
