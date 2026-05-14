datatype val_t =
   SBool of bool
 | SList of val_t list
val my_data : val_t = SList [
   SBool true,
   SBool false,
   SBool true
]
val _ = my_data
