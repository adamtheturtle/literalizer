Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "price $10",
            "$HOME"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "price $10",
            "$HOME"
        }
    End Sub
End Module
