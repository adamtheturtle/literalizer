void main() {
  {
    final my_data = <int>[
        1000000,
        -1234,
        255,
        -10,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <int>[
        1000000,
        -1234,
        255,
        -10,
    ];
    my_data.hashCode;
  }
}
