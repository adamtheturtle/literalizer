Imports System.Collections.Generic
Module Check
    ' heading
    ' actual comment
    ' final comment
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a", "single ' // data"},
        {"b", "linecontinuation"},
        {"c", "\"},
        {"d", "      "}
    }
End Module
