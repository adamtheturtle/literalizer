dynamic f({dynamic value}) => null;
final my_data = null;
void main() {
    final x = <List<int>>[
        <int>[
            1,
            2,
        ],
        <int>[
            3,
            4,
        ],
    ];
    f(value: <List<List<List<int>>>>[
        <List<List<int>>>[
            x,
        ],
    ]);
}
