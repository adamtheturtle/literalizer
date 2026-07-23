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
auto my_data = std::map<std::string, std::map<std::string, Value>>{
    {"level1", std::map<std::string, Value>{{"level2", std::map<std::string, Value>{{"level3", std::map<std::string, std::map<std::string, Value>>{{"level4", std::map<std::string, Value>{{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", std::vector<std::map<std::string, Value>>{std::map<std::string, Value>{{"name", "tag1"}, {"meta", std::map<std::string, Value>{{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
    (void)my_data;
    return 0;
}
