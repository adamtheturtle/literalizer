void _declaration() {
  final my_data = <String>[
      "48656c6c6f",
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String>[
      "48656c6c6f",
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
