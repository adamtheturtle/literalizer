#include <initializer_list>
#include <string>
#include <map>
struct Record1 { std::string name; int age{}; };
struct Record0 { int id{}; Record1 owner; };
int main() {
auto my_data = Record0{
    1,
    Record1{
        "Alice",
        30,
    },
};
    (void)my_data;
    return 0;
}
