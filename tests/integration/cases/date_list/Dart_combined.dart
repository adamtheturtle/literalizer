void _declaration() {
  final my_data = <DateTime>[
      DateTime.parse("2024-01-15"),
      DateTime.parse("2024-02-20"),
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <DateTime>[
      DateTime.parse("2024-01-15"),
      DateTime.parse("2024-02-20"),
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
