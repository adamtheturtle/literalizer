typedef enum {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
module check;
initial begin
_VVal my_data = '{
    "1", '{_VVAL_STR, 0, 0.0, "one"},
    "2", '{_VVAL_STR, 0, 0.0, "two"},
    "42", '{_VVAL_STR, 0, 0.0, "answer"}
};
end
endmodule
