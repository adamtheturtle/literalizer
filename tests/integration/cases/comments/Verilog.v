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
    // Server configuration
    "host", '{_VVAL_STR, 0, 0.0, "localhost"},  // default host
    "port", '{_VVAL_INT, 8080, 0.0, ""},
    // Enable debug mode
    "debug", '{_VVAL_INT, 1, 0.0, ""}
};
end
endmodule
