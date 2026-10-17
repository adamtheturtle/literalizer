module Check where


data Tuple a b = Tuple a b
data Val
    = PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)
    | PDict (Array (Tuple String Val))


my_data :: Val
my_data = PDict [
    (Tuple "below" (PList [
        PList [
            PList [
                PList [
                    PList [
                        PList [
                            PList [
                                PList [
                                    PInt 1
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ])),
    (Tuple "boundary" (PList [
        PList [
            PList [
                PList [
                    PList [
                        PList [
                            PList [
                                PList [
                                    PList [
                                        PInt 2
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ])),
    (Tuple "multiple" (PList [
        PList [
            PList [
                PList [
                    PList [
                        PList [
                            PList [
                                PList [
                                    PList [
                                        PList [
                                            PList [
                                                PList [
                                                    PList [
                                                        PList [
                                                            PList [
                                                                PList [
                                                                    PList [
                                                                        PInt 3
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
    ])),
    (Tuple "text" (PList [
        PList [
            PList [
                PList [
                    PList [
                        PList [
                            PList [
                                PList [
                                    PList [
                                        PStr "value"
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ])),
    (Tuple "boolean" (PList [
        PList [
            PList [
                PList [
                    PList [
                        PList [
                            PList [
                                PList [
                                    PList [
                                        PBool true
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ])),
    (Tuple "float" (PList [
        PList [
            PList [
                PList [
                    PList [
                        PList [
                            PList [
                                PList [
                                    PList [
                                        PFloat 1.5
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]
    ]))
]
