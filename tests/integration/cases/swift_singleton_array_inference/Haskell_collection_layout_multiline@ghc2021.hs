module Fixture_swift_singleton_array_inference_Haskell_collection_layout_multiline where
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("below", HList [
        HList [
            HList [
                HList [
                    HList [
                        HList [
                            HList [
                                HList [
                                    1
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]),
    ("boundary", HList [
        HList [
            HList [
                HList [
                    HList [
                        HList [
                            HList [
                                HList [
                                    HList [
                                        2
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]),
    ("multiple", HList [
        HList [
            HList [
                HList [
                    HList [
                        HList [
                            HList [
                                HList [
                                    HList [
                                        HList [
                                            HList [
                                                HList [
                                                    HList [
                                                        HList [
                                                            HList [
                                                                HList [
                                                                    HList [
                                                                        3
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
    ("text", HList [
        HList [
            HList [
                HList [
                    HList [
                        HList [
                            HList [
                                HList [
                                    HList [
                                        HStr "value"
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]),
    ("boolean", HList [
        HList [
            HList [
                HList [
                    HList [
                        HList [
                            HList [
                                HList [
                                    HList [
                                        HBool True
                                        ]
                                    ]
                                ]
                            ]
                        ]
                    ]
                ]
            ]
        ]),
    ("float", HList [
        HList [
            HList [
                HList [
                    HList [
                        HList [
                            HList [
                                HList [
                                    HList [
                                        1.5
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
main :: IO ()
main = seq my_data (return ())
