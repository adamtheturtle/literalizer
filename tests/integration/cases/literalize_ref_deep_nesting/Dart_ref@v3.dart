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
final my_data = <String, Map<String, Map<String, Map<String, String>>>>{
    "a": <String, Map<String, Map<String, String>>>{
        "b": <String, Map<String, String>>{
            "c": deep,
        },
    },
};
