#include <initializer_list>
#include <string>
#include <map>
#include <variant>
struct Record0 { std::string name; int age{}; bool active{}; double score{}; };
int main() {
auto my_data = Record0{
    .name = "Alice",
    .age = 30,
    .active = true,
    .score = 4.5,
};
    (void)my_data;
    return 0;
}
