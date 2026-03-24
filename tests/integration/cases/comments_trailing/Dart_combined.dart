void main() {
  {
    final my_data = <String>[
        "a",
        // trailing
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        "a",
        // trailing
    ];
    my_data.hashCode;
  }
}
