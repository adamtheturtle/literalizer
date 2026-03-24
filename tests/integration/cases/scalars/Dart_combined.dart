void main() {
  {
    final my_data = [
        42,
        3.14,
        true,
        false,
        "hello \"world\"",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        42,
        3.14,
        true,
        false,
        "hello \"world\"",
    ];
    my_data.hashCode;
  }
}
