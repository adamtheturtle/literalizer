#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Record1 { int id{}; std::string description; bool is_done{}; std::vector<int> blocks; };
struct Record0 { std::string project; Record1 lead_task; };
int main() {
auto my_data = Record0{
    "alpha",
    Record1{
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
my_data = Record0{
    "alpha",
    Record1{
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
