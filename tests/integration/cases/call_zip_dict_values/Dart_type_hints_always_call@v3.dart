dynamic process({dynamic value}) => null;
dynamic emit(dynamic _call, dynamic _zip) => null;
final my_data = null;
void main() {
    emit(process(value: "hello"), <String, int>{"a": 1, "b": 2});
    emit(process(value: 42), <String, int>{"c": 3, "d": 4});
}
