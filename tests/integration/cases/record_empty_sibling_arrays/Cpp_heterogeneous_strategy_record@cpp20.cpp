#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <variant>
struct Record1 { int item{}; };
struct Record2 { std::nullptr_t item{}; };
struct Record0 { std::vector<std::vector<Record1>> integers; std::vector<std::vector<Record2>> nulls; std::vector<std::vector<std::vector<Record1>>> nested; std::vector<std::vector<Record1>> reversed; };
int main() {
auto my_data = Record0{
    .integers = std::vector{
        std::vector<Record1>{},
        std::vector{
            Record1{
                .item = 1,
            },
        },
    },
    .nulls = std::vector{
        std::vector<Record2>{},
        std::vector{
            Record2{
                .item = nullptr,
            },
        },
    },
    .nested = std::vector{
        std::vector{
            std::vector<Record1>{},
            std::vector{
                Record1{
                    .item = 2,
                },
            },
        },
        std::vector{
            std::vector{
                Record1{
                    .item = 3,
                },
            },
            std::vector<Record1>{},
        },
    },
    .reversed = std::vector{
        std::vector{
            Record1{
                .item = 4,
            },
        },
        std::vector<Record1>{},
    },
};
    (void)my_data;
    return 0;
}
