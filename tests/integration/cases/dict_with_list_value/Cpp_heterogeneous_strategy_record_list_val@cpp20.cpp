#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record0 { std::string name; std::vector<int> scores; };
int main() {
auto my_data = Record0{
    .name = "Alice",
    .scores = std::vector<int>{
        10,
        20,
        30,
    },
};
    (void)my_data;
    return 0;
}
