#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
#include <cstddef>
struct Record0 { std::vector<std::pair<std::string, std::variant<std::vector<std::vector<long long>>, std::string>>> values; bool flag{}; std::vector<std::vector<long long>> direct_arrays; };
int main() {
auto my_data = Record0{
    .values = {
        {"wide", std::vector<std::vector<long long>>{
            std::vector<long long>{
                2208988800,
            },
            std::vector<long long>{},
        }},
        {"narrow", std::vector<std::vector<long long>>{
            std::vector<long long>{
                946684800,
            },
        }},
        {"negative", std::vector<std::vector<long long>>{
            std::vector<long long>{
                -2208988800,
            },
        }},
        {"shifted", std::vector<std::vector<long long>>{
            std::vector<long long>{
                2208988800,
            },
        }},
        {"mixed_width", std::vector<std::vector<long long>>{
            std::vector<long long>{
                946684800,
            },
            std::vector<long long>{
                2208988800,
            },
        }},
        {"text", "preserve"},
    },
    .flag = true,
    .direct_arrays = {
        std::vector<long long>{
            2208988800,
        },
        std::vector<long long>{},
    },
};
    (void)my_data;
    return 0;
}
