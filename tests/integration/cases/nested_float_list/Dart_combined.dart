void _declaration() {
  final my_data = <List<double>>[
      <double>[1.5, 2.5],
      <double>[3.5, 4.5],
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <List<double>>[
      <double>[1.5, 2.5],
      <double>[3.5, 4.5],
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
