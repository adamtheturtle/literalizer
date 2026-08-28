#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct Record1 { int status{}; };
struct Record2 { std::string status; };
struct Record4 { std::string kind; bool urgent{}; };
struct Record3 { Record4 inner; };
struct Record6 { std::string error; };
struct Record5 { Record6 inner; };
struct Record7 { Record1 holder; };
struct Record8 { Record2 holder; };
struct Record9 { std::vector<long long> nums; };
struct Record0 { Record1 plain; Record2 other; Record3 nested_a; Record5 nested_b; Record7 wrap_a; Record8 wrap_b; Record9 wide; };
int main() {
auto my_data = Record0{
    .plain = {
        .status = 1,
    },
    .other = {
        .status = "ready",
    },
    .nested_a = {
        .inner = {
            .kind = "add",
            .urgent = true,
        },
    },
    .nested_b = {
        .inner = {
            .error = "not_found",
        },
    },
    .wrap_a = {
        .holder = {
            .status = 2,
        },
    },
    .wrap_b = {
        .holder = {
            .status = "word",
        },
    },
    .wide = {
        .nums = {
            1,
            1099511627776,
        },
    },
};
    (void)my_data;
    return 0;
}
