dynamic f({dynamic ops}) => null;
final my_data = null;
void main() {
    f(ops: <List<String>>[<String>["DEL", "b", "10"], <String>["ADD", "a", "x"]]);  // note
    // next call
    f(ops: <List<String>>[<String>["ADD", "c", "y"]]);
}
