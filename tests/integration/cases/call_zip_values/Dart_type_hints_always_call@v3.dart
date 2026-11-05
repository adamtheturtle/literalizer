dynamic process({dynamic value}) => null;
dynamic emit({dynamic argument0, dynamic argument1}) => null;
final my_data = null;
void main() {
    emit(argument0: process(value: "hello"), argument1: true);
    emit(argument0: process(value: 42), argument1: false);
}
