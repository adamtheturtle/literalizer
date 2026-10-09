#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record0 { int id{}; std::string label; bool enabled{}; std::vector<int> related_ids; };
int main() {
auto my_data = Record0{
    1,
    "She said \"hello\", then waved",
    false,
    {
        1,
        2,
        3,
    },
};
    (void)my_data;
    return 0;
}
