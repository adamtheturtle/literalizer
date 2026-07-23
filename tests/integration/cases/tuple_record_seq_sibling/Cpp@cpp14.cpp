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
auto my_data = std::map<std::string, Value>{
    {"scores", std::vector<int>{10, 20, 30}},
    {"args", std::vector<Value>{1, "email", "a@gmail.com", 100}},
};
    (void)my_data;
    return 0;
}
