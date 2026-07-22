#include <initializer_list>
#include <string>
#include <map>
struct Record0 { std::string name; int age{}; bool active{}; double score{}; };
int main() {
auto my_data = Record0{
    "Alice",
    30,
    true,
    4.5,
};
(void)my_data;
my_data = Record0{
    "Alice",
    30,
    true,
    4.5,
};
    (void)my_data;
    return 0;
}
