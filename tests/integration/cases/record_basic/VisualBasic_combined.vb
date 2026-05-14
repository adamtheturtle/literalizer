Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"id", 1},
            {"description", "She said ""hello"", then waved"},
            {"is_done", False},
            {"blocks", New Integer() {1, 2, 3}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"id", 1},
            {"description", "She said ""hello"", then waved"},
            {"is_done", False},
            {"blocks", New Integer() {1, 2, 3}}
        }
    End Sub
End Module
