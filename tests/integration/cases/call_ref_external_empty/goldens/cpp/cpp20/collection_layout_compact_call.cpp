#include <vector>
#include <utility>
auto consume(auto...) { return 0; }
int main() {
auto item = std::vector<int>{
    1,
    2,
};
consume(std::move(item));
    return 0;
}
