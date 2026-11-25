#include <vector>
#include <string>
struct Record0 { int a{}; std::string b; };
int main() {

    auto my_data = std::vector<Record0>{Record0{
    .a = 1,
    .b = "x",
}};
    (void)my_data;
    return 0;
}
