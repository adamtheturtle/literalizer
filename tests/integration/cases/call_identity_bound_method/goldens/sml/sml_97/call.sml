datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
structure thing = struct
fun go _ = ()
end
val item : val_t = SList [
    SInt 1,
    SInt 2
]
val _ = thing.go(item)
