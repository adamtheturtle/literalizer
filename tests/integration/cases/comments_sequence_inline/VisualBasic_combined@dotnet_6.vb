Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' note a
        ' note b
        Dim my_data = New String() {
            "a",
            "b"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' note a
        ' note b
        my_data = New String() {
            "a",
            "b"
        }
    End Sub
End Module
