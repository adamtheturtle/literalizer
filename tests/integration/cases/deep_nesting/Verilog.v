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
    "level1", '{"level2", '{"level3", '{"level4", '{"value", '{_VVAL_STR, 0, 0.0, "deep"}, "items", '{'{_VVAL_STR, 0, 0.0, "a"}, '{_VVAL_STR, 0, 0.0, "b"}}}}, "sibling", '{_VVAL_INT, 42, 0.0, ""}}, "tags", '{'{"name", '{_VVAL_STR, 0, 0.0, "tag1"}, "meta", '{"priority", '{_VVAL_INT, 1, 0.0, ""}, "labels", '{'{_VVAL_STR, 0, 0.0, "x"}, '{_VVAL_STR, 0, 0.0, "y"}}}}}}
};
end
endmodule
