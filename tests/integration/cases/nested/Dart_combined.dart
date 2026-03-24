void main() {
  {
    final my_data = {
        "users": [{"name": "Bob", "tags": <String>["admin", "user"]}, {"name": "Carol", "tags": <String>["guest"]}],
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "users": [{"name": "Bob", "tags": <String>["admin", "user"]}, {"name": "Carol", "tags": <String>["guest"]}],
    };
    my_data.hashCode;
  }
}
