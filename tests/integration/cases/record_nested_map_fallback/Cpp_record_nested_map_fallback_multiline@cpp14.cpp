#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
template <typename... Types> struct LiteralizerVariant { template <typename T> LiteralizerVariant(T) {} // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
using LiteralizerRecordValue = LiteralizerVariant<std::string, bool, std::nullptr_t>;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> input; std::map<std::string, LiteralizerRecordValue> expected; };
int main() {
auto my_data = std::vector{
    Record0{
        "test_1",
        std::map<std::string, LiteralizerRecordValue>{
            {"type", LiteralizerRecordValue{"create"}},
            {"pr_id", LiteralizerRecordValue{"pr_1"}},
            {"draft", LiteralizerRecordValue{true}},
            {"missing", LiteralizerRecordValue{nullptr}},
        },
        std::map<std::string, LiteralizerRecordValue>{
            {"pr_id", LiteralizerRecordValue{"pr_1"}},
            {"status", LiteralizerRecordValue{"draft"}},
        },
    },
    Record0{
        "test_2",
        std::map<std::string, LiteralizerRecordValue>{
            {"type", LiteralizerRecordValue{"publish"}},
            {"pr_id", LiteralizerRecordValue{"pr_1"}},
        },
        std::map<std::string, LiteralizerRecordValue>{
            {"error", LiteralizerRecordValue{"invalid_operation"}},
        },
    },
};
    (void)my_data;
    return 0;
}
