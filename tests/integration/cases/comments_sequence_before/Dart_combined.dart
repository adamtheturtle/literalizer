void _declaration() {
  final my_data = <String>[
      // first
      "a",
      // second
      "b",
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String>[
      // first
      "a",
      // second
      "b",
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
