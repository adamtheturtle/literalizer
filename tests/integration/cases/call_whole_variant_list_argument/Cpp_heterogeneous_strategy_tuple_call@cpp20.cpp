#include <tuple>
auto f(auto...) { return 0; }
int main() {
f(std::make_tuple(1, "x"));
    return 0;
}
