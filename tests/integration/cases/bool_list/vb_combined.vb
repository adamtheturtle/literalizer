Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Boolean() {
            True,
            False,
            True
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Boolean() {
            True,
            False,
            True
        }
    End Sub
End Module
