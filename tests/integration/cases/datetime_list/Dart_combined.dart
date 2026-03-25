void main() {
  {
    final my_data = <DateTime>[
        DateTime.parse("2024-01-15T12:30:00.123456+00:00"),
        DateTime.parse("2024-06-01T08:00:00+00:00"),
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <DateTime>[
        DateTime.parse("2024-01-15T12:30:00.123456+00:00"),
        DateTime.parse("2024-06-01T08:00:00+00:00"),
    ];
    my_data.hashCode;
  }
}
