void _declaration() {
  final my_data = <List<bool>>[
      <bool>[true, false],
      <bool>[true, true],
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <List<bool>>[
      <bool>[true, false],
      <bool>[true, true],
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
