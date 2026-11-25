final deep = <List<String>>[
    <String>[
        "one",
        "two",
    ],
    <String>[
        "three",
        "four",
    ],
];
final my_data = <String, Map<String, Map<String, List<List<String>>>>>{
    "a": <String, Map<String, List<List<String>>>>{
        "b": <String, List<List<String>>>{
            "c": deep,
        },
    },
};
