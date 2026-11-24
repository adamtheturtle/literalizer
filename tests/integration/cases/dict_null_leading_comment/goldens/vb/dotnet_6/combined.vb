Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' comment
        Dim my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"score", Nothing}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' comment
        my_data = New Dictionary(Of String, Object) From {
            {"name", "Alice"},
            {"score", Nothing}
        }
    End Sub
End Module
