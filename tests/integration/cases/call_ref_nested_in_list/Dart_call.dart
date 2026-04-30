dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final my_var = 42;
    final my_other = 7;
    process(data: [<String, String>{"ref": "my_var"}, 42, "static"]);
    process(data: [<String, String>{"ref": "my_other"}, 7, "label"]);
}
