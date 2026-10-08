structure helper = struct
fun list _ = ()
end
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = helper.list(SInt 1)
