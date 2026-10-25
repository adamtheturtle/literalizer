datatype val_t =
    SStr of string
val my_data : val_t = SStr (* coding: ascii *)
"caf\195\169"
val _ = my_data
