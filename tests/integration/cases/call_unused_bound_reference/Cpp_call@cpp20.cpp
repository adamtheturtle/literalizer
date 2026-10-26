#include <vector>
auto f(auto...) { return 0; }
int main() {
f(std::vector<int>{1, 2});
    return 0;
}
