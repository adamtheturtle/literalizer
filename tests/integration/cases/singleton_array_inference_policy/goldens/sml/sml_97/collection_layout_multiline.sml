datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("below", SList [
        SList [
            SList [
                SList [
                    SList [
                        SList [
                            SList [
                                SList [
                                    SInt 1
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]),
    ("boundary", SList [
        SList [
            SList [
                SList [
                    SList [
                        SList [
                            SList [
                                SList [
                                    SList [
                                        SInt 2
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]),
    ("multiple", SList [
        SList [
            SList [
                SList [
                    SList [
                        SList [
                            SList [
                                SList [
                                    SList [
                                        SList [
                                            SList [
                                                SList [
                                                    SList [
                                                        SList [
                                                            SList [
                                                                SList [
                                                                    SList [
                                                                        SInt 3
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
    ]),
    ("text", SList [
        SList [
            SList [
                SList [
                    SList [
                        SList [
                            SList [
                                SList [
                                    SList [
                                        SStr "value"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]),
    ("boolean", SList [
        SList [
            SList [
                SList [
                    SList [
                        SList [
                            SList [
                                SList [
                                    SList [
                                        SBool true
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]),
    ("float", SList [
        SList [
            SList [
                SList [
                    SList [
                        SList [
                            SList [
                                SList [
                                    SList [
                                        SReal 1.5
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
val _ = my_data
