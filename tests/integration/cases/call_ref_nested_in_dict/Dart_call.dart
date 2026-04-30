dynamic process({dynamic data}) => null;
final my_data = null;
void main() {
    final my_var = 42;
    process(data: <String, dynamic>{"key": <String, String>{"ref": "my_var"}, "count": 42});
}
