#include <type_traits>
template<class T, class U=T> struct Node {};
template<class T, std::enable_if_t<(sizeof(T) == 0), int> = 0> void accept(T) {}
void accept(...) {}
int main() { ::accept(Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<int>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}); }
