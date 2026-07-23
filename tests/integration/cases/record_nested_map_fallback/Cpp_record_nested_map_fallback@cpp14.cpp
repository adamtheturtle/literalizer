#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
#include <vector>
#include <memory>
#include <utility>
struct Value {
 private:
  struct Holder { virtual ~Holder() {} };
  template <typename T> struct TypedHolder : Holder {
    explicit TypedHolder(T value) : value(std::move(value)) {}
    T value;
  };
  std::shared_ptr<Holder> value_;
 public:
  Value() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> Value(T value) : value_(new TypedHolder<T>(std::move(value))) {}
  template <typename T> bool is() const {
    return dynamic_cast<TypedHolder<T>*>(value_.get()) != nullptr;
  }
  template <typename T> T& get() {
    return static_cast<TypedHolder<T>*>(value_.get())->value;
  } // get
  template <typename T> const T& get() const {
    return static_cast<const TypedHolder<T>*>(value_.get())->value;
  } // get const
};
using LiteralizerRecordValue = Value;
struct Record0 { std::string name; std::map<std::string, LiteralizerRecordValue> input; std::map<std::string, LiteralizerRecordValue> expected; };
int main() {
auto my_data = std::vector{
    Record0{"test_1", std::map<std::string, LiteralizerRecordValue>{{"type", LiteralizerRecordValue{"create"}}, {"pr_id", LiteralizerRecordValue{"pr_1"}}, {"draft", LiteralizerRecordValue{true}}, {"missing", LiteralizerRecordValue{nullptr}}}, std::map<std::string, LiteralizerRecordValue>{{"pr_id", LiteralizerRecordValue{"pr_1"}}, {"status", LiteralizerRecordValue{"draft"}}}},
    Record0{"test_2", std::map<std::string, LiteralizerRecordValue>{{"type", LiteralizerRecordValue{"publish"}}, {"pr_id", LiteralizerRecordValue{"pr_1"}}}, std::map<std::string, LiteralizerRecordValue>{{"error", LiteralizerRecordValue{"invalid_operation"}}}},
};
    (void)my_data;
    return 0;
}
