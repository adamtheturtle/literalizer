Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", New Object() {}},
            {"b", New Object() {}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Object() {}},
            {"b", New Object() {}}
        }
    End Sub
End Module
