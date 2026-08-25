datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SInt 2, SStr "hello"],  (* trailing note *)
    (* next element *)
    SList [SInt 3, SStr "world"]
]
val _ = my_data
