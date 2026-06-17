dynamic record_value({dynamic value}) => null;
dynamic flush_buffer({dynamic count}) => null;
dynamic emit(dynamic _arg) => null;
final my_data = null;
void main() {
    emit(record_value(value: 42));
    flush_buffer(count: 3);
}
