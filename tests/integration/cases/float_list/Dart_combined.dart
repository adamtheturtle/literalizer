void main() {
  {
    final my_data = <double>[
        1.1,
        2.2,
        3.3,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <double>[
        1.1,
        2.2,
        3.3,
    ];
    my_data.hashCode;
  }
}
