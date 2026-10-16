datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val ref_data : val_t = SList [
    SInt 1,
    SInt 2
]
val my_data : val_t = SList [
    SInt 0
]
(void)my_data;
val my_data : val_t = ref_data
(void)my_data;
