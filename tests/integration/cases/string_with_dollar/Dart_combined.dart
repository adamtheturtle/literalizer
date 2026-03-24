void main() {
  {
    final my_data = <String>[
        "price \$10",
        "\$HOME",
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String>[
        "price \$10",
        "\$HOME",
    ];
    my_data.hashCode;
  }
}
