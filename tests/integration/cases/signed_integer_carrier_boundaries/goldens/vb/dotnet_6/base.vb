Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"i32_below", -2147483649},
        {"i32_minimum", -2147483648},
        {"i32_above", -2147483647},
        {"i32_maximum", 2147483647},
        {"i32_over", 2147483648},
        {"i64_minimum", Long.MinValue},
        {"i64_maximum", 9223372036854775807}
    }
End Module
