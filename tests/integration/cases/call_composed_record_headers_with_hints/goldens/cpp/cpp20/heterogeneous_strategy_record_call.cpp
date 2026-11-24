#include <string>
#include <vector>
struct Record0 { std::string name; std::vector<int> values; };
auto consume(auto...) { return 0; }
int main() {
auto item = Record0{
    .name = "first",
    .values = {
        1,
        2,
    },
};
consume(item);
    return 0;
}
