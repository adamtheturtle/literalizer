typedef enum {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
module check;
initial begin
// note
_VVal my_data = '{_VVAL_INT, 42, 0.0, ""};
end
endmodule
