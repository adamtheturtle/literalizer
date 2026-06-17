fun put _ = ()
fun get _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = put(1, 10)
val _ = get(1)
