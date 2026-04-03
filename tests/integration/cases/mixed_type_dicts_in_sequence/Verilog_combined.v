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
    '{"type", '{_VVAL_STR, 0, 0.0, "create"}, "pr_id", '{_VVAL_STR, 0, 0.0, "pr_1"}, "draft", '{_VVAL_INT, 1, 0.0, ""}},
    '{"type", '{_VVAL_STR, 0, 0.0, "create"}, "pr_id", '{_VVAL_STR, 0, 0.0, "pr_2"}}
};
my_data = '{
    '{"type", '{_VVAL_STR, 0, 0.0, "create"}, "pr_id", '{_VVAL_STR, 0, 0.0, "pr_1"}, "draft", '{_VVAL_INT, 1, 0.0, ""}},
    '{"type", '{_VVAL_STR, 0, 0.0, "create"}, "pr_id", '{_VVAL_STR, 0, 0.0, "pr_2"}}
};
end
endmodule
