#include <initializer_list>
#include <vector>
#include <cstddef>
auto consume(auto...) { return 0; }
int main() {
auto item = std::vector<int>{
    1,
    2,
};
consume(std::move(item));
    return 0;
}
