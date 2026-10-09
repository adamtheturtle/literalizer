#include <initializer_list>
#include <string>
struct Record1 { int x{}; };
struct Record2 { std::string day; std::string stamp; };
struct Record0 { Record1 plain; Record2 timed; };
int main() {
auto plain = Record1{
    1,
};
auto timed = Record2{
    "2001-01-02",
    "2001-01-02T03:04:05+00:00",
};
auto my_data = Record0{
    plain,
    std::move(timed),
};
    (void)my_data;
    return 0;
}
