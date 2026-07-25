#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record0 { int id{}; std::string label; bool enabled{}; std::vector<int> related_ids; };
int main() {
auto my_data = Record0{
    .id = 1,
    .label = "She said \"hello\", then waved",
    .enabled = false,
    .related_ids = std::vector<int>{
        1,
        2,
        3,
    },
};
    (void)my_data;
    return 0;
}
