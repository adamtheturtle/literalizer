#include <initializer_list>
#include <string>
#include <map>
struct Record1 { std::string x; };
struct Record2 { int x{}; };
struct Record0 { Record1 direct; Record2 bound; };
int main() {
auto first = Record2{
    1,
};
auto my_data = std::map<std::string, std::map<std::string, Value>>{
    {"direct", std::map<std::string, Value>{{"x", "s"}}},
    {"bound", std::move(first)},
};
    (void)my_data;
    return 0;
}
