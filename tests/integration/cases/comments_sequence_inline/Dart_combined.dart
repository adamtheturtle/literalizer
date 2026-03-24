void main() {
  {
    final my_data = <String>[
        "a",  // note a
        "b",  // note b
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        "a",  // note a
        "b",  // note b
    ];
    my_data.hashCode;
  }
}
