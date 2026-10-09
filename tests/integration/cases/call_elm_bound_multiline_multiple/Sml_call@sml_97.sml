datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
val ref_data : val_t = SList [
    SInt 1,
    SInt 2
]
val _ = f(SList [
    ref_data
])
val _ = f(SList [
    ref_data
])
