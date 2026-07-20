#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
struct Record1 { int id{}; std::string label; };
struct Record0 { std::string name; std::vector<Record1> items; };
int main() {
auto my_data = Record0{
    .name = "box",
    .items = std::vector{
        Record1{
            .id = 1,
            .label = "first",
        },
        Record1{
            .id = 2,
            .label = "second",
        },
    },
};
    (void)my_data;
    return 0;
}
