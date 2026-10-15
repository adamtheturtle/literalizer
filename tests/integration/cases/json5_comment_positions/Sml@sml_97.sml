datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    (* *)
    (* document heading *)
    (* before the first entry *)
    (* after the key *)
    (* before the value *)
    ("counts", SList [
        (* before the first item *)
        SInt 1,  (* inline block after the comma *)
        (* before the second item *)
        SInt 2
        (* trailing inside the array *)
    ]),  (* after the nested collection *)
    ("more", SList [
        SInt 3,
        (* *)
        (* block heading *)
        (* block continuation *)
        SInt 4  (* final inline *)
    ])
    (* trailing inside the object *)
    (* after the root *)
    (* after the document *)
]
val _ = my_data
