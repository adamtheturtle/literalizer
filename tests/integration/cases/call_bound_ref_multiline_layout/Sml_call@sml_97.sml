datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun f _ = ()
val ref_data : val_t = SList [
    SList [
        SInt 1,
        SInt 2
    ],
    SList [
        SInt 3,
        SInt 4
    ]
]
val _ = f(SList [
    SList [
        ref_data
    ]
])
