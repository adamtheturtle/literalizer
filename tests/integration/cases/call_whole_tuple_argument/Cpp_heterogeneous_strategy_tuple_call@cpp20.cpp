#include <tuple>
auto process(auto...) { return 0; }
int main() {
process(std::make_tuple("hello", 42, true));
    return 0;
}
