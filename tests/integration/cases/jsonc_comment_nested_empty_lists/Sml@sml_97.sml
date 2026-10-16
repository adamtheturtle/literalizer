datatype val_t =
    SList of val_t list
val my_data : val_t = SList [
    (* outer heading *)
    (* first empty *)
    SList [],
    (* second empty *)
    SList []
]
val _ = my_data
