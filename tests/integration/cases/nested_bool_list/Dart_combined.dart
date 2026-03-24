void main() {
  {
    final my_data = <List<bool>>[
        <bool>[true, false],
        <bool>[true, true],
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <List<bool>>[
        <bool>[true, false],
        <bool>[true, true],
    ];
    my_data.hashCode;
  }
}
