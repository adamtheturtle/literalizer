void main() {
  {
    final my_data = <String, String>{
        "key\nwith\nnewlines": "value1",
        "key\twith\ttabs": "value2",
        "": "value3",
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String, String>{
        "key\nwith\nnewlines": "value1",
        "key\twith\ttabs": "value2",
        "": "value3",
    };
    my_data.hashCode;
  }
}
