#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Record0 { int id{}; std::string description; bool is_done{}; std::vector<int> blocks; };
int main() {
auto my_data = Record0{
    1,
    "She said \"hello\", then waved",
    false,
    std::vector<int>{
        1,
        2,
        3,
    },
};
(void)my_data;
my_data = Record0{
    1,
    "She said \"hello\", then waved",
    false,
    std::vector<int>{
        1,
        2,
        3,
    },
};
    (void)my_data;
    return 0;
}
