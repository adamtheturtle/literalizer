#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
#include <map>
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
struct Record1 { int item{}; };
struct Record2 { std::nullptr_t item{}; };
struct Record0 { std::vector<std::vector<std::map<std::string, int>>> integers; std::vector<Value> nulls; std::vector<std::vector<std::vector<std::map<std::string, int>>>> nested; std::vector<std::vector<std::map<std::string, int>>> reversed; };
int main() {
auto my_data = Record0{
    std::vector<Value>{
        std::vector<Record1>{},
        std::vector<Record1>{
            Record1{
                1,
            },
        },
    },
    {
        Value{std::vector<Record2>{}},
        Value{std::vector<Record2>{
            Record2{
                nullptr,
            },
        }},
    },
    std::vector<Value>{
        std::vector<std::vector<std::map<std::string, int>>>{
            std::vector<Record1>{},
            std::vector<Record1>{
                Record1{
                    2,
                },
            },
        },
        std::vector<std::vector<std::map<std::string, int>>>{
            std::vector<Record1>{
                Record1{
                    3,
                },
            },
            std::vector<Record1>{},
        },
    },
    std::vector<Value>{
        std::vector<Record1>{
            Record1{
                4,
            },
        },
        std::vector<Record1>{},
    },
};
    (void)my_data;
    return 0;
}
