import QtQuick 2.1

Rectangle {
    id: rectangle
    color: "red"
    width: 200
    height: 200

    Text {
        id: text
        text: "This is QML code.\n(Tap to pause)"
        font.pointSize: 34
        anchors.centerIn: parent
        PropertyAnimation {
            id: animation
            target: text
            property: "rotation"
            from: 0; to: 360; duration: 5000
            loops: Animation.Infinite
        }
    }
    MouseArea {
        anchors.fill: parent
        onClicked: animation.paused ? animation.resume() : animation.pause()
    }
    Component.onCompleted: animation.start()
}
