dynamic process({dynamic value}) => null;
class _TracerType { dynamic emit(dynamic _arg) => null; }
final tracer = _TracerType();
final my_data = null;
void main() {
    tracer.emit(process(value: "hello"));
    tracer.emit(process(value: 42));
    tracer.emit(process(value: true));
}
