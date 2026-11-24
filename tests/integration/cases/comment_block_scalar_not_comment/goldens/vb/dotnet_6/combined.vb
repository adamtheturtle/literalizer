Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"description", "# not a comment" & Chr(10)},
            {"name", "foo"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"description", "# not a comment" & Chr(10)},
            {"name", "foo"}
        }
    End Sub
End Module
