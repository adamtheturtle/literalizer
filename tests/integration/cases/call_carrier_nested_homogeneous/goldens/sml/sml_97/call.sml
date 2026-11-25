structure app = struct
structure client = struct
fun go _ = ()
end
end
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = app.client.go(SList [SInt 1], SList [SInt 2])
