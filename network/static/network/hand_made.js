document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector("#createPostForm");
    if (form) {
        form.onsubmit = function(event) {
            event.preventDefault();
            document.querySelector("#timeStamp").value = new Date().toISOString();
            console.log("Timestamp set to:", document.querySelector("#timeStamp").value);
            form.submit();
        }
    }
    else{
    }

    initProfileButtonLinks();
    initNavButtonLinks("AllPostbutton");
    likeButtonIncrement();
    dislikeButtonIncrement();
    followButtonLogic();
    editButtonLogic();
   
    
});

function initNavButtonLinks(buttonID) {
    try {
        console.log("Button clicked!");
        var buttons = document.querySelectorAll('.Navbutton');
       
        buttons.forEach(function(button) {
            button.addEventListener('click', function() {
                window.location.href = button.getAttribute("data-url");
            });
        });
    } catch (error) {
        console.error("An error occurred in initNavButtonLinks:", error);
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function likeButtonIncrement() {
    var likeButtons = document.querySelectorAll(".likeButton");
    var dislikeButtons = document.querySelectorAll(".dislikeButtons");

    if (!likeButtons.length) {
        console.warn("Like button not found in the DOM.");
        return; 
    }

    if (!dislikeButtons.length) {
        console.warn("Dislike button not found in the DOM.");
        return; 
    }

    likeButtons.forEach(function(likeButton) {
        var postID = likeButton.getAttribute("data-postid");
        var user = likeButton.getAttribute("data-user");
        var csrftoken = getCookie('csrftoken'); 

        var dislikeButton = document.querySelector(`.dislikeButtons[data-postid="${postID}"]`);

        likeButton.onclick = function() {
            fetch('/incrementLikes', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user: user,
                    postID: postID
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                likeButton.innerHTML = `👍 Likes: ${data.likes}`;
                
                if (data.changebutton === "True") {
                    dislikeButton.innerHTML = `👎 Dislikes: ${data.dislikes}`; 
                    likeButton.innerHTML = `👍 Likes: ${data.likes}`;  
                }
            })
            .catch(error => console.error('Error:', error));
        };
    });
}




function dislikeButtonIncrement() { 
    var likeButtons = document.querySelectorAll(".likeButton");
    var dislikeButtons = document.querySelectorAll(".dislikeButtons"); 

    if (!likeButtons.length) {
        console.warn("Like button not found in the DOM.");
        return; 
    }

    if (!dislikeButtons.length) {
        console.warn("Dislike button not found in the DOM.");
        return; 
    }
    dislikeButtons.forEach(function(dislikeButton) { 
        var postID = dislikeButton.getAttribute("data-postid");
        var user = dislikeButton.getAttribute("data-user");
        var csrftoken = getCookie('csrftoken'); 
        var likeButton = document.querySelector(`.likeButton[data-postid="${postID}"]`);

        dislikeButton.onclick = function() {
            fetch('/incrementDislikes', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user: user,
                    postID: postID
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                dislikeButton.innerHTML = `👎 Dislikes: ${data.dislikes}`;
           
                if (data.changeLikeButton === "True") {
                    console.log("ChangeButton is true");
                    likeButton.innerHTML = `👍 Likes: ${data.likes}`;
                    dislikeButton.innerHTML = `👎 Dislikes: ${data.dislikes}`;
                }
            })
            .catch(error => console.error('Error:', error));
        };
    });
}

function initProfileButtonLinks() {
    try {
        var profileButtons = document.querySelectorAll(".LHS");
        console.log("Found profile buttons: ", profileButtons);
        profileButtons.forEach(function(profileButton) {
            profileButton.addEventListener('click', function(event) {
                console.log("Button clicked:", profileButton);
                var url = profileButton.getAttribute("data-url");
                console.log("Redirecting to URL: " + url);
                if (url) {
                    window.location.href = url;
                } else {
                    console.error("URL not found for profile button");
                }
            });
        });
    } catch (error) {
        console.error("An error occurred in initProfileButtonLinks:", error);
    }
}

function editButtonLogic() {
    var editButtons = document.querySelectorAll(".editButton");

    editButtons.forEach(function(editButton) {
        editButton.onclick = function() {
            var count = 0;
            if (editButton.innerHTML == "Edit") {
                var textarea = document.createElement("textarea");
                textarea.id = "editTextArea";
                var postID = editButton.getAttribute("data-postid");

                var postBody = document.querySelector(`.postBody[data-postid="${postID}"]`);

                textarea.value = postBody.innerHTML;
                postBody.parentNode.replaceChild(textarea, postBody);
                textarea.style.width = "100%";

                editButton.innerHTML = "Save";
                count = 1;
            }

            if (editButton.innerHTML == "Save" && count == 0) {
                var postBody = document.querySelector("#editTextArea").value;
                var postBodyObject = document.querySelector("#editTextArea");
                console.log(postBody);
                count = 0;

                var postID = editButton.getAttribute("data-postid");
                var postBodySpan = document.createElement("span");
                postBodySpan.className = "postBody";
                postBodySpan.setAttribute("data-postid", postID);

                fetch('/editPost', {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        postID: postID,
                        postBody: postBody
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    postBodySpan.innerHTML = postBody;
                    postBodyObject.parentNode.replaceChild(postBodySpan, postBodyObject);
                    editButton.innerHTML = "Edit";
                    console.log(data.message);
                })
                .catch(error => console.error('Error:', error));
            }
        };
    });
}

function followButtonLogic(){
     var followButtons = document.querySelectorAll(".followButton");
        
     followButtons.forEach(function(followButton) {
        followButton.onclick = function() {
            var userProfile = followButton.getAttribute("data-userProfile");
            var profileUserFollowersHeader = document.querySelector(`.user_followers_count[data-userProfile="${userProfile}"]`);

            var followStatus = followButton.innerHTML;

            console.log(followStatus);
            console.log(userProfile);
            
            var csrftoken = getCookie('csrftoken');

             fetch('/followUser', {
                method: 'POST',
                headers:{
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                },
                 body: JSON.stringify({
                    userProfile: userProfile,
                    followStatus: followStatus
                })
             })
             .then(response => response.json())
             .then(data => {
                profileUserFollowersHeader.innerHTML = `Followers: ${data.followers}`;
                followButton.innerHTML = data.followStatus;
             })
            
        }
     });
}

