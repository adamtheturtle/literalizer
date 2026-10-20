datatype val_t =
    SStr of string
val source_value : val_t = SStr "\239\191\190\239\191\191"
val my_data : val_t = source_value
val _ = my_data
