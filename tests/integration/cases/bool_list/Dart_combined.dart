void main() {
  {
    final my_data = <bool>[
        true,
        false,
        true,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <bool>[
        true,
        false,
        true,
    ];
    my_data.hashCode;
  }
}
