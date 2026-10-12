#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record1 { int id{}; std::string label; };
struct Record0 { std::string name; std::vector<Record1> items; };
int main() {
auto my_data = Record0{
    "box",
    std::vector{
        Record1{
            1,
            "first",
        },
        Record1{
            2,
            "second",
        },
    },
};
    (void)my_data;
    return 0;
}
