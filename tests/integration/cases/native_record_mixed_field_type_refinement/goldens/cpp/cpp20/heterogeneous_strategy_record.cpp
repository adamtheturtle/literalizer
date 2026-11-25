#include <string>
#include <variant>
#include <vector>
struct Record2 { int value{}; };
struct Record1 { std::vector<std::variant<int, Record2>> items; };
struct Record4 { std::string value; };
struct Record3 { std::vector<std::variant<int, Record4>> items; };
struct Record0 { Record1 first; Record3 second; };
int main() {
auto my_data = Record0{
    .first = {
        .items = {
            1,
            Record2{
                .value = 2,
            },
        },
    },
    .second = {
        .items = {
            1,
            Record4{
                .value = "s",
            },
        },
    },
};
    (void)my_data;
    return 0;
}
