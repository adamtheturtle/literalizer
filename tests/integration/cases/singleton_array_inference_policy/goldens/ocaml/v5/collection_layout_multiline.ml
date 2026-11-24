module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OFloat of float
  | OStr of string
  | OList of val_t list
  | OMap of (string * val_t) list
let my_data : val_t = OMap [
    ("below", OList [
        OList [
            OList [
                OList [
                    OList [
                        OList [
                            OList [
                                OList [
                                    OInt 1
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("boundary", OList [
        OList [
            OList [
                OList [
                    OList [
                        OList [
                            OList [
                                OList [
                                    OList [
                                        OInt 2
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("multiple", OList [
        OList [
            OList [
                OList [
                    OList [
                        OList [
                            OList [
                                OList [
                                    OList [
                                        OList [
                                            OList [
                                                OList [
                                                    OList [
                                                        OList [
                                                            OList [
                                                                OList [
                                                                    OList [
                                                                        OInt 3
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
    ("text", OList [
        OList [
            OList [
                OList [
                    OList [
                        OList [
                            OList [
                                OList [
                                    OList [
                                        OStr "value"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("boolean", OList [
        OList [
            OList [
                OList [
                    OList [
                        OList [
                            OList [
                                OList [
                                    OList [
                                        OBool true
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]);
    ("float", OList [
        OList [
            OList [
                OList [
                    OList [
                        OList [
                            OList [
                                OList [
                                    OList [
                                        OFloat 1.5
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

end
