void _declaration() {
  final my_data = <String>[
      "line1\nline2",
      "line1line2",
      "",
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String>[
      "line1\nline2",
      "line1line2",
      "",
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
