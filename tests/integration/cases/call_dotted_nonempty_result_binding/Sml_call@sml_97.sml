structure thing = struct
fun go _ = ()
end
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val my_data = thing.go(SList [SInt 1])
val _ = my_data
