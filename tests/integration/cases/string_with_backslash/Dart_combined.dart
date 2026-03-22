void _declaration() {
  final my_data = <String>[
      "C:\\path\\to\\file",
      "back\\\\slash",
      "hello \\\"world\\\"",
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String>[
      "C:\\path\\to\\file",
      "back\\\\slash",
      "hello \\\"world\\\"",
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
