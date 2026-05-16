#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record0 { int id{}; std::string description; bool is_done{}; std::vector<int> blocks; };
int main() {
auto my_data = Record0{
    .id = 1,
    .description = "She said \"hello\", then waved",
    .is_done = false,
    .blocks = std::vector<int>{
        1,
        2,
        3,
    },
};
    (void)my_data;
    return 0;
}
