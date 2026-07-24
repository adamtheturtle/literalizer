#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct NamedType { int id{}; std::string description; bool is_done{}; std::vector<int> blocks; };
struct Record0 { std::string project; NamedType lead_task; };
int main() {
auto my_data = Record0{
    "alpha",
    NamedType{
        100,
        "first task",
        false,
        std::vector<int>{
            102,
            103,
        },
    },
};
    (void)my_data;
    return 0;
}
