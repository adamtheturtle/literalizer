module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [
        FMap [
            ("mapping", FMap [])
        ];
        FMap []
    ];
    FList [
        FMap [];
        FMap [
            ("mapping", FMap [])
        ]
    ]
]
