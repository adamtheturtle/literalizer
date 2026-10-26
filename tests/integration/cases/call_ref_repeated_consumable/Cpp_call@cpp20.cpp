#include <vector>
auto process(auto...) { return 0; }
int main() {
auto item = std::vector<int>{
    1,
    2,
};
process(item);
process(item);
    return 0;
}
