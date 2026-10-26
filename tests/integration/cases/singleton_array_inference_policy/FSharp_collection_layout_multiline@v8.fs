module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("below", FList [
        FList [
            FList [
                FList [
                    FList [
                        FList [
                            FList [
                                FList [
                                    FInt 1L
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("boundary", FList [
        FList [
            FList [
                FList [
                    FList [
                        FList [
                            FList [
                                FList [
                                    FList [
                                        FInt 2L
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("multiple", FList [
        FList [
            FList [
                FList [
                    FList [
                        FList [
                            FList [
                                FList [
                                    FList [
                                        FList [
                                            FList [
                                                FList [
                                                    FList [
                                                        FList [
                                                            FList [
                                                                FList [
                                                                    FList [
                                                                        FInt 3L
                                                                    ]
                                                                ]
                                                            ]
                                                        ]
                                                    ]
                                                ]
                                            ]
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("text", FList [
        FList [
            FList [
                FList [
                    FList [
                        FList [
                            FList [
                                FList [
                                    FList [
                                        FStr "value"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("boolean", FList [
        FList [
            FList [
                FList [
                    FList [
                        FList [
                            FList [
                                FList [
                                    FList [
                                        FBool true
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("float", FList [
        FList [
            FList [
                FList [
                    FList [
                        FList [
                            FList [
                                FList [
                                    FList [
                                        FFloat 1.5
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ])
]
