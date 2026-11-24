#include <vector>
struct Record0 { bool active{}; };
int main() {
auto my_data = std::vector<Record0>{
    Record0{true},
    Record0{false},
};
    (void)my_data;
    return 0;
}
