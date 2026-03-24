void main() {
  {
    final my_data = <String>[
        // line 1
        // line 2
        "a",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        // line 1
        // line 2
        "a",
    ];
    my_data.hashCode;
  }
}
