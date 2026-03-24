void main() {
  {
    final my_data = {
        DateTime.parse("2024-01-15"),
        DateTime.parse("2024-06-01"),
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        DateTime.parse("2024-01-15"),
        DateTime.parse("2024-06-01"),
    };
    my_data.hashCode;
  }
}
