void main() {
  {
    final my_data = <double>[
        1,
        2.5,
        3,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <double>[
        1,
        2.5,
        3,
    ];
    my_data.hashCode;
  }
}
