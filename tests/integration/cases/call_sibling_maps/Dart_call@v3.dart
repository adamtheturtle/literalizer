dynamic process({dynamic value}) => null;
final my_data = null;
void main() {
    process(value: <String, dynamic>{"value": 1});
    process(value: <String, dynamic>{"value": "hello"});
}
