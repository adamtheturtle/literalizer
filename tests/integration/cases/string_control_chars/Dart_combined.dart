void main() {
  {
    final my_data = <String>[
        "line1\r\nline2",
        "line1\rline2",
        "",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        "line1\r\nline2",
        "line1\rline2",
        "",
    ];
    my_data.hashCode;
  }
}
