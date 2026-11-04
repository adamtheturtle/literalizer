structure thing = struct
fun go _ = ()
end
datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val _ = thing.go(SList [], SList [SInt 1], SList [])
val _ = thing.go(SList [SStr "text"], SList [SInt 2], SList [])
val _ = thing.go(SList [], SList [SStr "text"], SList [])
val _ = thing.go(SList [SStr "text"], SList [SInt 2], SList [SInt 3])
