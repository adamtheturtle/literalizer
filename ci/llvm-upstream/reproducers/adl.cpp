namespace assoc {
struct Leaf {};
template<class T, class U=T> struct Node {};
void consume(...);
}
void test(assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Leaf>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> value) { consume(value); }
