proc consume {args} {}
set foo 42
consume [list
    [dict create
        "other" 1
    ]
    foo
] [dict create
    "left" foo
    "other" 1
]
