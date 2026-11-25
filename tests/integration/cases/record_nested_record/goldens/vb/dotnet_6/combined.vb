Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"id", 1},
            {"owner", New Dictionary(Of String, Object) From {{"name", "Alice"}, {"age", 30}}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"id", 1},
            {"owner", New Dictionary(Of String, Object) From {{"name", "Alice"}, {"age", 30}}}
        }
    End Sub
End Module
