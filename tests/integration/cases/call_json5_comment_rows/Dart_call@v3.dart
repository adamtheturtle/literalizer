dynamic f({dynamic a, dynamic b}) => null;
final my_data = null;
void main() {
    // calls heading
    // before call one
    // first argument
    f(a: 1, b: 2);  // after call one
    // second argument
    f(a: 3, b: 4);
    // after all calls
}
