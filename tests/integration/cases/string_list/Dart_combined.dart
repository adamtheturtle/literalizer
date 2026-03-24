void main() {
  {
    final my_data = <String>[
        "foo",
        "bar",
        "baz",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        "foo",
        "bar",
        "baz",
    ];
    my_data.hashCode;
  }
}
