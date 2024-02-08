document.addEventListener("DOMContentLoaded", function () {
    const createGroupButton = document.getElementById("create-group-submit");
    const joinGroupButton = document.getElementById("join-group-submit");

    createGroupButton.addEventListener("click", function () {
        window.location.href = "/chat/create_room"; 
    });

    joinGroupButton.addEventListener("click", function () {
        window.location.href = "/chat/join_room";
    });
});