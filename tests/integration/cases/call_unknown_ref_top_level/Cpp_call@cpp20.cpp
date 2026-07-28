#include <initializer_list>
#include <vector>
#include <cstddef>
auto process(auto...) { return 0; }
int main() {
auto unknown_value = std::vector<int>{
    1,
};
process(unknown_value);
    return 0;
}
