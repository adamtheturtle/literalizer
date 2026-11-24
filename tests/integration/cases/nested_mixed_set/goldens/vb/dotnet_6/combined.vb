Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"tags", New HashSet(Of Object) From {True, 42, "apple"}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"tags", New HashSet(Of Object) From {True, 42, "apple"}}
        }
    End Sub
End Module
