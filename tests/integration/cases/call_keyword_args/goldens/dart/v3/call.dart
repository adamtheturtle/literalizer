class _ThrottlerType { dynamic check({dynamic user_id, dynamic ts}) => null; }
final throttler = _ThrottlerType();
dynamic emit(dynamic _arg) => null;
final my_data = null;
void main() {
    emit(throttler.check(user_id: "user_1", ts: 1000.0));
    emit(throttler.check(user_id: "user_2", ts: 2000.5));
}
