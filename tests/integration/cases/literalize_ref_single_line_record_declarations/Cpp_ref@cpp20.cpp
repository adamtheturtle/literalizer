#include <initializer_list>
#include <string>
#include <map>
struct Record1 { std::string x; };
struct Record2 { int x{}; };
struct Record0 { Record1 direct; Record2 bound; };
#include <variant>
int main() {
auto first = Record2{
    .x = 1,
};
auto my_data = Record0{
    .direct = {
        .x = "s",
    },
    .bound = std::move(first),
};
    (void)my_data;
    return 0;
}
