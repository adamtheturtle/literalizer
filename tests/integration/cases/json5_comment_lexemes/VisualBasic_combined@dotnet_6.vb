Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' heading
        ' actual comment
        ' final comment
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", "single ' // data"},
            {"b", "linecontinuation"},
            {"c", "\"},
            {"d", "          "}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' heading
        ' actual comment
        ' final comment
        my_data = New Dictionary(Of String, Object) From {
            {"a", "single ' // data"},
            {"b", "linecontinuation"},
            {"c", "\"},
            {"d", "          "}
        }
    End Sub
End Module
