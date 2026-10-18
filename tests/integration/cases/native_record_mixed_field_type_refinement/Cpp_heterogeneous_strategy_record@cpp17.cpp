#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record2 { int value{}; };
struct Record1 { std::vector<std::variant<int, Record2>> items; };
struct Record4 { std::string value; };
struct Record3 { std::vector<std::variant<int, Record4>> items; };
struct Record0 { Record1 first; Record3 second; };
int main() {
auto my_data = Record0{
    {
        {
            1,
            Record2{
                2,
            },
        },
    },
    {
        {
            1,
            Record4{
                "s",
            },
        },
    },
};
    (void)my_data;
    return 0;
}
