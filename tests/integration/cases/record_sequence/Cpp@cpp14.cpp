#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <cstddef>
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
int main() {
auto my_data = std::vector<std::map<std::string, Value>>{
    std::map<std::string, Value>{{"id", 1}, {"label", "first"}, {"tags", std::vector<std::nullptr_t>{}}},
    std::map<std::string, Value>{{"id", 2}, {"label", "second"}, {"tags", std::vector<std::nullptr_t>{}}},
    std::map<std::string, Value>{{"id", 3}, {"label", "third"}, {"tags", std::vector<std::nullptr_t>{}}},
};
    (void)my_data;
    return 0;
}
