#include <initializer_list>
#include <string>
#include <map>
#include <variant>
struct Record1 { std::string name; int age{}; };
struct Record0 { int id{}; Record1 owner; };
int main() {
auto my_data = Record0{
    .id = 1,
    .owner = Record1{
        .name = "Alice",
        .age = 30,
    },
};
    (void)my_data;
    return 0;
}
