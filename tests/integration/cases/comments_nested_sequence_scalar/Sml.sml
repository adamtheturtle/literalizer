datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SStr "ADD", SStr "alice", SStr "hello"],
    SList [SStr "DEL", SStr "bob", SStr "5"]  (* removes "world" *)
]
val _ = my_data
