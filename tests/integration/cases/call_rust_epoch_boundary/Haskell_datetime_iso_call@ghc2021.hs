module Fixture_call_rust_epoch_boundary_Haskell_datetime_iso_call where
consume :: Val -> IO ()
consume _ = return ()
data Val = HList [Val] | HStr String
main :: IO ()
main = do
    _ <- consume (HStr "1901-12-13T20:45:51")
    _ <- consume (HStr "2038-01-19T03:14:08")
    pure ()
