void main() {
  {
    final my_data = <String>[
        // first
        "a",
        // second
        "b",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        // first
        "a",
        // second
        "b",
    ];
    my_data.hashCode;
  }
}
