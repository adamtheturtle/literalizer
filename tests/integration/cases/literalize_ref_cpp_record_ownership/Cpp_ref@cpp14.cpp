#include <initializer_list>
#include <string>
#include <cstddef>
struct Record1 { int integer{}; bool boolean{}; double decimal{}; std::nullptr_t null{}; };
struct Record3 { int integer{}; };
struct Record2 { Record3 child; };
struct Record4 { std::string text; };
struct Record5 { std::string day; std::string stamp; };
struct Record0 { Record1 trivial; Record2 nested; Record4 owning; Record5 calendar; };
int main() {
auto trivial = Record1{
    1,
    true,
    1.5,
    nullptr,
};
auto nested = Record2{
    {
        2,
    },
};
auto owning = Record4{
    "owned",
};
auto calendar = Record5{
    "2001-01-02",
    "2001-01-02T03:04:05+00:00",
};
auto my_data = Record0{
    trivial,
    nested,
    std::move(owning),
    std::move(calendar),
};
    (void)my_data;
    return 0;
}
