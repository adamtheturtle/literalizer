#include <cstddef>
#include <string>
#include <unordered_map>
#include <vector>
#include <memory>
#include <utility>
struct Value {
 private:
  struct Holder {
    Holder() = default;
    Holder(const Holder&) = delete;
    Holder(Holder&&) = delete;
    Holder& operator=(const Holder&) = delete;
    Holder& operator=(Holder&&) = delete;
    virtual ~Holder() = default;
  };
  template <typename T> struct TypedHolder : Holder {
    explicit TypedHolder(T value) : value_(std::move(value)) {}
    T& get() { return value_; }
    const T& get() const { return value_; }
   private:
    T value_;
  }; // TypedHolder
  static std::shared_ptr<Holder> make_holder(const char* value) {
    return std::make_shared<TypedHolder<std::string>>(value);
  } // make_holder string
  template <typename T> static std::shared_ptr<Holder> make_holder(T value) {
    return std::make_shared<TypedHolder<T>>(std::move(value));
  } // make_holder generic
  std::shared_ptr<Holder> value_;
 public:
  Value() : value_(new TypedHolder<std::nullptr_t>(nullptr)) {}
  template <typename T> explicit Value(T value) : value_(make_holder(std::move(value))) {}
  template <typename T> bool is() const {
    return dynamic_cast<TypedHolder<T>*>(value_.get()) != nullptr;
  }
  template <typename T> T& get() {
    return static_cast<TypedHolder<T>*>(value_.get())->get();
  } // get
  template <typename T> const T& get() const {
    return static_cast<const TypedHolder<T>*>(value_.get())->get();
  } // get const
};
int main() {
auto my_data = std::vector<std::unordered_map<std::string, Value>>{
    std::unordered_map<std::string, Value>{{"name", Value{"Ada"}}, {"active", Value{true}}, {"count", Value{1}}, {"score", Value{1.5}}, {"missing", Value{nullptr}}, {"scores", Value{std::vector<int>{1, 2}}}, {"child", Value{std::unordered_map<std::string, int>{{"age", 3}}}}},
    std::unordered_map<std::string, Value>{{"name", Value{"Bob"}}, {"active", Value{false}}, {"count", Value{2}}, {"score", Value{2.5}}, {"missing", Value{nullptr}}, {"scores", Value{std::vector<int>{4}}}, {"child", Value{std::unordered_map<std::string, int>{{"age", 5}}}}},
};
    (void)my_data;
    return 0;
}
