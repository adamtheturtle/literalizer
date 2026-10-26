datatype val_t =
    SInt of LargeInt.int
  | SSet of val_t list
val my_data : val_t = SSet [
    SInt 10,  (* comment for ten *)
    SInt 2  (* comment for two *)
]
val _ = my_data
