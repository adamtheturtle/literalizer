#include <map>
#include <string>
#include <vector>
#include <cstddef>
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
auto my_data = std::map<std::string, std::map<std::string, Value>>{
    {"true_to_one", std::map<std::string, Value>{{"value", Value{1}}}},
    {"one_to_true", std::map<std::string, Value>{{"value", Value{true}}}},
    {"false_to_zero", std::map<std::string, Value>{{"value", Value{0}}}},
    {"zero_to_false", std::map<std::string, Value>{{"value", Value{false}}}},
    {"nested_boolean_to_float", std::map<std::string, Value>{{"value", Value{std::vector<double>{1.0}}}}},
    {"nested_float_to_boolean", std::map<std::string, Value>{{"value", Value{std::vector<bool>{false}}}}},
    {"nested_value_types_changed", std::map<std::string, Value>{{"value", Value{std::map<std::string, Value>{{"nested", std::vector<Value>{Value{true}, Value{0}}}}}}}},
    {"nested_value_types_reversed", std::map<std::string, Value>{{"value", Value{std::map<std::string, Value>{{"nested", std::vector<Value>{Value{1}, Value{false}}}}}}}},
    {"array_order_changed", std::map<std::string, Value>{{"value", Value{std::vector<int>{2, 1}}}}},
    {"array_length_changed", std::map<std::string, Value>{{"value", Value{std::vector<int>{1, 2}}}}},
    {"null_to_zero", std::map<std::string, Value>{{"value", Value{0}}}},
    {"string_to_boolean", std::map<std::string, Value>{{"value", Value{true}}}},
    {"object_key_changed", std::map<std::string, Value>{{"value", Value{std::map<std::string, Value>{{"b", 1}}}}}},
};
    (void)my_data;
    return 0;
}
