Imports System.Collections.Generic
Module Check
    Sub _declaration()
        '
        ' document heading
        ' before the first entry
        ' after the key
        ' before the value
        ' before the first item
        ' inline block after the comma
        ' before the second item
        ' trailing inside the array
        ' after the nested collection
        '
        ' block heading
        ' block continuation
        ' final inline
        ' trailing inside the object
        ' after the root
        ' after the document
        Dim my_data = New Dictionary(Of String, Object) From {
            {"counts", New Integer() {1, 2}},
            {"more", New Integer() {3, 4}}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        '
        ' document heading
        ' before the first entry
        ' after the key
        ' before the value
        ' before the first item
        ' inline block after the comma
        ' before the second item
        ' trailing inside the array
        ' after the nested collection
        '
        ' block heading
        ' block continuation
        ' final inline
        ' trailing inside the object
        ' after the root
        ' after the document
        my_data = New Dictionary(Of String, Object) From {
            {"counts", New Integer() {1, 2}},
            {"more", New Integer() {3, 4}}
        }
    End Sub
End Module
