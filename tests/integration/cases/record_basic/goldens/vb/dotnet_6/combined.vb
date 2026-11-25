Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"id", 1},
            {"label", "She said ""hello"", then waved"},
            {"enabled", False},
            {"related_ids", New Integer() {1, 2, 3}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"id", 1},
            {"label", "She said ""hello"", then waved"},
            {"enabled", False},
            {"related_ids", New Integer() {1, 2, 3}}
        }
    End Sub
End Module
