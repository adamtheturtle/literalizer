#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(std::vector<int>{
    1,
    2,
});
process(std::vector<int>{
    3,
});
    return 0;
}
