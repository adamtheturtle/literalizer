dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    var shared = 42;
    consume(value: shared);
}
