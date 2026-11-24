datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val ref_data : val_t = SInt 1
val my_data : val_t = ref_data
val _ = my_data
