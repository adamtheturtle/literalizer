module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OList [
    OList [
        OMap [
            ("values", OList [
                OList []
            ])
        ];
        OMap []
    ];
    OList [
        OMap [];
        OMap [
            ("values", OList [
                OList []
            ])
        ]
    ]
]

end
