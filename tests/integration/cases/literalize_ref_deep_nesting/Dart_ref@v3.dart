final deep = <List<int>>[
    <int>[
        1,
        2,
    ],
    <int>[
        3,
        4,
    ],
];
final my_data = <String, Map<String, Map<String, List<List<int>>>>>{
    "a": <String, Map<String, List<List<int>>>>{
        "b": <String, List<List<int>>>{
            "c": deep,
        },
    },
};
