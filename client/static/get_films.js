let container = document.getElementById('videos')


fetch("http://localhost:3000/").then((Response) => {
        return Response.json()
    }).then((data) => {
        for (let index = 0; index < data.length; index++) {
            data[index] = 'q=' + data[index] + '&';
            
        }
        console.log(data.join(''));

        fetch("http://localhost:80/list/?" + data.join('')).then((Response) => {
                return Response.json()
            }).then((data) => {
                console.log(data);
                data.forEach(element => {
                    container.innerHTML +='<iframe id="video" width="560" height="315" src="https://www.youtube.com/embed/' + element['id'] + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'

                });
            });
    })