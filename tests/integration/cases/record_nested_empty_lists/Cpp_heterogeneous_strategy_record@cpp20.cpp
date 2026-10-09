#include <initializer_list>
#include <string>
#include <vector>
#include <cstddef>
struct Record0 { std::vector<std::vector<int>> a; std::vector<std::vector<int>> b; };
int main() {
auto my_data = Record0{
    .a = {
        std::vector<int>{
            1,
            2,
        },
        std::vector<int>{
            3,
        },
    },
    .b = {
        std::vector<int>{},
        std::vector<int>{
            1,
        },
    },
};
    (void)my_data;
    return 0;
}
