#include <initializer_list>
#include <vector>
auto f(auto...) { return 0; }
int main() {
auto ref_data = std::vector<std::vector<int>>{
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
        ref_data,
    },
});
    return 0;
}
