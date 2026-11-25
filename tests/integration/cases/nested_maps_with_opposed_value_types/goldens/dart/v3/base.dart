final my_data = <Map<String, Map<String, dynamic>>>[
    <String, Map<String, dynamic>>{"input": <String, dynamic>{"name": "alice", "city": "paris"}, "expected": <String, dynamic>{"count": 1, "total": 2}},
    <String, Map<String, dynamic>>{"input": <String, dynamic>{"name": 10, "city": 20}, "expected": <String, dynamic>{"count": "done", "total": "pending"}},
];
