final my_data = null;
void main() {
    final shared = <int>[
        1,
        2,
    ];
    var my_data = <int>[
        0,
    ];
    _ = &my_data;
    my_data = shared;
    _ = &my_data;
}
