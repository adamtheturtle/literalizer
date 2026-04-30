dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final myVar = 42;
    process(data: [<String, String>{"ref": "myVar"}, 42, "static"]);
}
