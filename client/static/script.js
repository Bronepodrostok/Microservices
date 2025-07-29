btn = document.getElementById('gen_btn')
let video = document.getElementById('video')
let current = 0

btn.onclick = async function() {

    fetch("http://localhost:80/").then((Response) => {
        return Response.json()
    }).then((data) => {
        current = data["id"]
        video.src = "https://www.youtube.com/embed/" + data["id"]
    })

    
}
btn.click()
add = document.getElementById('add')

add.onclick = async function(){

    fetch("http://localhost:3000/?id=" + current, {
    method: "POST"
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
}



