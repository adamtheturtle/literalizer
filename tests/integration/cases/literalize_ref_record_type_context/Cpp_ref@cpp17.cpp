#include <initializer_list>
#include <string>
#include <variant>
struct Record1 { std::string x; };
struct Record2 { int x{}; };
struct Record0 { Record1 direct; Record2 bound; };
int main() {
auto first = Record2{
    1,
};
auto my_data = Record0{
    {
        "s",
    },
    first,
};
    (void)my_data;
    return 0;
}
