dynamic consume({dynamic value}) => null;
final my_data = null;
void main() {
    consume(value: "1901-12-13T20:45:51");
    consume(value: "2038-01-19T03:14:08");
}
