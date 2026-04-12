typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
typedef struct {
    string k;
    _VVal v;
} _VKV;
module check;
initial begin
class _throttler_t;
  function void check(string a, real b); endfunction
endclass
_throttler_t throttler = new;
function automatic void print(string a); endfunction
print(throttler.check("user_1", 1000.0))
print(throttler.check("user_2", 2000.5))
end
endmodule
