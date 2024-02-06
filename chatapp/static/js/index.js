document.addEventListener("DOMContentLoaded", function () {
    const createGroupButton = document.getElementById("create-group-submit");
    const joinGroupButton = document.getElementById("join-group-submit");

    createGroupButton.addEventListener("click", function () {
        window.location.href = "/chat/create_room"; // Replace with your desired URL
    });

    joinGroupButton.addEventListener("click", function () {
        window.location.href = "/chat/join"; // Replace with your desired URL
    });
});