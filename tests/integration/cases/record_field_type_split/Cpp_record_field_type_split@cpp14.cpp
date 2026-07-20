#include <initializer_list>
#include <string>
#include <map>
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
    .plain = Record1{
        .status = 1,
    },
    .other = Record2{
        .status = "ready",
    },
    .nested_a = Record3{
        .inner = Record4{
            .kind = "add",
            .urgent = true,
        },
    },
    .nested_b = Record5{
        .inner = Record6{
            .error = "not_found",
        },
    },
    .wrap_a = Record7{
        .holder = Record1{
            .status = 2,
        },
    },
    .wrap_b = Record8{
        .holder = Record2{
            .status = "word",
        },
    },
    .wide = Record9{
        .nums = std::vector<long long>{
            1,
            1099511627776,
        },
    },
};
    (void)my_data;
    return 0;
}
