#include <vector>
struct Record1 { int a{}; };
struct Record0 { std::vector<Record1> items; };
int main() {
auto my_data = Record0{
    std::vector{
        Record1{
            1,
        },
    },
};
    (void)my_data;
    return 0;
}
