void _declaration() {
  final my_data = <String>[
      // line 1
      // line 2
      "a",
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String>[
      // line 1
      // line 2
      "a",
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
