#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
auto item = std::vector<int>{
    1,
    2,
};
process(std::vector<std::vector<int>>{item, item});
    return 0;
}
