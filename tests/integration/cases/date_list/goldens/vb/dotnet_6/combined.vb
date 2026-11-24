Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New DateOnly() {
            New DateOnly(2024, 1, 15),
            New DateOnly(2024, 2, 20)
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New DateOnly() {
            New DateOnly(2024, 1, 15),
            New DateOnly(2024, 2, 20)
        }
    End Sub
End Module
