final my_data = null;
void main() {
    final ref_data = <int>[
        1,
        2,
    ];
    final my_data = <int>[
        0,
    ];
    (void)my_data;
    my_data = ref_data;
    (void)my_data;
}
