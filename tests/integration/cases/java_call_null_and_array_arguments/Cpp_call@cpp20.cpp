#include <initializer_list>
#include <cstddef>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process(nullptr);
process(std::vector<int>{1, 2});
    return 0;
}
