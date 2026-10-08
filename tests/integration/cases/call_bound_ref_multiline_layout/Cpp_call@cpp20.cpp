#include <initializer_list>
#include <vector>
auto f(auto...) { return 0; }
int main() {
auto x = std::vector<std::vector<int>>{
    std::vector<int>{
        1,
        2,
    },
    std::vector<int>{
        3,
        4,
    },
};
f(std::vector<std::vector<std::vector<std::vector<int>>>>{
    std::vector<std::vector<std::vector<int>>>{
        x,
    },
});
    return 0;
}
