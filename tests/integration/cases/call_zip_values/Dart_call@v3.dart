dynamic process({dynamic value}) => null;
dynamic emit(dynamic _call, dynamic _zip) => null;
final my_data = null;
void main() {
    emit(process(value: "hello"), 1);
    emit(process(value: 42), 0);
}
