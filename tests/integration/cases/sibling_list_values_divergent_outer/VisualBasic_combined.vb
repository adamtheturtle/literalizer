Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", New Object() {1}},
            {"b", New Object() {"x"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Object() {1}},
            {"b", New Object() {"x"}}
        }
    End Sub
End Module
