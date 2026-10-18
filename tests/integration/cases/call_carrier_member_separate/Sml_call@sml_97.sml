structure app = struct
fun go _ = ()
end
datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val _ = app.go(SList [SInt 1], SList [SStr "text"])
