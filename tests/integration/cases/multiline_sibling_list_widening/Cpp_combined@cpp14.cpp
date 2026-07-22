#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <utility>
struct Record1 { std::vector<int> numbers; std::vector<std::string> strings; };
struct Record0 { std::vector<std::pair<std::string, int>> omap_value; Record1 sibling_lists; std::vector<std::string> ref_marker_present; };
int main() {
auto my_data = Record0{
    std::vector<std::pair<std::string, int>>{
        {"first", 1},
    },
    Record1{
        std::vector<int>{
            1,
            2,
        },
        std::vector<std::string>{
            "x",
            "y",
        },
    },
    std::vector<std::string>{
        "$keep",
        "z",
    },
};
(void)my_data;
my_data = Record0{
    std::vector<std::pair<std::string, int>>{
        {"first", 1},
    },
    Record1{
        std::vector<int>{
            1,
            2,
        },
        std::vector<std::string>{
            "x",
            "y",
        },
    },
    std::vector<std::string>{
        "$keep",
        "z",
    },
};
    (void)my_data;
    return 0;
}
