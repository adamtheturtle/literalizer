dynamic f({dynamic a, dynamic b}) => null;
final my_data = null;
void main() {
    f(a: 2, b: "hello");  // trailing note
    f(a: 3, b: "world");  // another note
}
