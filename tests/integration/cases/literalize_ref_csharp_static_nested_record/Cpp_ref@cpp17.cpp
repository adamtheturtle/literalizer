#include <initializer_list>
#include <string>
#include <variant>
struct Record1 { std::string x; };
struct Record2 { int x{}; };
struct Record0 { Record1 direct; Record2 bound; };
int main() {
auto ref_data = Record2{
    1,
};
static auto my_data = Record0{
    {
        "s",
    },
    ref_data,
};
    (void)my_data;
    return 0;
}
