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
    "my-key", '{_VVAL_STR, 0, 0.0, "value1"},
    "another-key", '{_VVAL_STR, 0, 0.0, "value2"},
    "normal_key", '{_VVAL_STR, 0, 0.0, "value3"}
};
end
endmodule
