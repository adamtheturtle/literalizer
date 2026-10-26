#include <vector>
auto f(auto...) { return 0; }
int main() {
f(std::vector<std::vector<int>>{std::vector<int>{1, 2}, std::vector<int>{3}});
    return 0;
}
