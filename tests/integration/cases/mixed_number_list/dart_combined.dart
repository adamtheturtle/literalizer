void _declaration() {
  final my_data = <double>[
      1,
      2.5,
      3,
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <double>[
      1,
      2.5,
      3,
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
