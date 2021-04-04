document.addEventListener('DOMContentLoaded', function(){
    let editviews = document.querySelectorAll('#edit-view');
    editviews.forEach(p => {
        p.style.display = "none";
    })
    let ids = document.querySelectorAll('#postId');
    ids.forEach(i =>{
        i.style.display = "none";
    })
})

function editButton(element) {
    console.log(element)
    let p1 = element.parentElement;
    p1.querySelector("#toweetContent").style.display = "none";
    p1.querySelector("#toweetDate").style.display = "none";
    p1.querySelector('#edit-view').style.display = "block";
}

function saveButton(element) {
    let a1 = element.parentElement.parentElement;
    let a2 = a1.querySelector('#postId');
    let a3 = a1.querySelector('textarea').value;
    a1.querySelector('#edit-view').style.display = "none";
    a1.querySelector('#toweetContent').innerHTML = a1.querySelector('textarea').value;
    a1.querySelector('#toweetContent').style.display = 'block';
    a1.querySelector("#toweetDate").style.display = "block";
    editToweet(a2.innerHTML, a3);
}
function myFunction(x, element) {
    if(x.classList == "fa fa-thumbs-o-up") {
        x.classList.remove("fa.fa-thumbs-o-up");
        x.classList.add("fa-thumbs-up");
        PostLike(element);
  }
    else {
        x.classList.remove("fa-thumbs-up");
        x.classList.add("fa-thumbs-o-up");
        PostUnlike(element);
    }
}

function PostLike(element) {
  fetch(`/Post/${element.innerHTML}`, {
    method: 'PUT',
    body: JSON.stringify({
        PostLikes: true
    })})
  .then(response => response.json())
  .then(toweet => {
      console.log(toweet)
      element.previousElementSibling.innerHTML = toweet.PostLikes;
  })
}
      // ... Adding like count by one ...

function PostUnlike(element) {
    fetch(`/Post/${element.innerHTML}`, {
        method: 'PUT',
        body: JSON.stringify({
            PostLikes: false
        })})
    .then(response => response.json())
    .then(toweet => {
        console.log(toweet);
        element.previousElementSibling.innerHTML = toweet.PostLikes;
        // ... Subtracting like count by one ...
    })}


function editToweet(id, toweetBody) {
        fetch(`/Post/update/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              newToweetContent: toweetBody
          })})
        .then(response => response.json())
        .then(toweet => {
            console.log(toweet)
        })
            // ... Updating toweet ...
        }