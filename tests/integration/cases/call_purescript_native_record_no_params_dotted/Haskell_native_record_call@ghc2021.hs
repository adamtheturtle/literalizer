{-# LANGUAGE DuplicateRecordFields #-}
{-# LANGUAGE OverloadedRecordDot #-}
module Fixture_call_purescript_native_record_no_params_dotted_Haskell_native_record_call where
data ClientType_ = ClientType_ { consume :: IO () }
data AppType_ = AppType_ { client :: ClientType_ }
app :: AppType_
app = AppType_ { client = ClientType_ { consume = return () } }
main :: IO ()
main = do
    _ <- app.client.consume
    pure ()
