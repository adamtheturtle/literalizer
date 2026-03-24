void main() {
  {
    final my_data = <String>[
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        "C:\\path\\to\\file",
        "back\\\\slash",
        "hello \\\"world\\\"",
    ];
    my_data.hashCode;
  }
}
