void main() {
  {
    final my_data = <int>[
        1,
        2,
        3,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <int>[
        1,
        2,
        3,
    ];
    my_data.hashCode;
  }
}
