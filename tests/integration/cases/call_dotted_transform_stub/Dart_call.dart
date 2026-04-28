dynamic process({dynamic value}) => null;
class _LogType { dynamic emit(dynamic _arg) => null; }
final log = _LogType();
final my_data = null;
void main() {
    log.emit(process(value: "hello"));
    log.emit(process(value: 42));
    log.emit(process(value: true));
}
