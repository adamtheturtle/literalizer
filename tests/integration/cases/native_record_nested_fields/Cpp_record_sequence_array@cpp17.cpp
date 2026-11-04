#include <vector>
#include <string>
struct Record1 { std::string name; bool active{}; };
struct Record2 { std::string name; double score{}; };
struct Record0 { Record1 owner; std::vector<Record2> members; };
int main() {
auto my_data = Record0{
    {
        "Ada",
        false,
    },
    std::vector{
        Record2{
            "Ada",
            1.5,
        },
        Record2{
            "Bob",
            2.5,
        },
    },
};
    (void)my_data;
    return 0;
}
