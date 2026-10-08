module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let f _ = ()
let ref_data : val_t = OList [
    OList [
        OInt 1;
        OInt 2
    ];
    OList [
        OInt 3;
        OInt 4
    ]
]
let _ = f(OList [
    OList [
        ref_data
    ]
])

end
