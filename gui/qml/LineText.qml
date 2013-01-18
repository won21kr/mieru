//LineText.qml
import QtQuick 1.1
import com.nokia.meego 1.1

Item {
    id: lineTextMain

    height: label.height

    property alias text: label.text

    Rectangle {
        id: line
        color : "white"
        height : 2

        anchors {
            left: parent.left
            right : label.left
            rightMargin : 8
            verticalCenter: parent.verticalCenter
        }
    }

    Label {
        id: label
        lineHeight : 1.5
        font.pointSize : 20

        anchors {
            top: parent.top
            //left: parent.left
            right: parent.right
            leftMargin: 16
            rightMargin: 16
        }
    }
}