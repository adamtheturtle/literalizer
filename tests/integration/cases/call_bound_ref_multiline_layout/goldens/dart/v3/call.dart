dynamic f({dynamic value}) => null;
final my_data = null;
void main() {
    final ref_data = <List<int>>[
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
            ref_data,
        ],
    ]);
}
