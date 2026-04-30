datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(1, 0, 3600)  (* Jan 1 1970 00:00:00 - 01:00:00 *)
val _ = process(5, 0, 3600)  (* Jan 1 1970 00:00:05 - 01:00:05 *)
val _ = process(2, 0, 5400)  (* Jan 1 1970 00:00:02 - 01:30:02 *)
