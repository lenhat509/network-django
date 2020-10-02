document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.post').forEach( post => {
        post.querySelector('#toggle-like').onclick =  () => {
            const data = {
                method: "POST",
                credentials:'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.cookie.split(';').find(c => c.startsWith('csrftoken')).split('=')[1]
                },
                body: JSON.stringify({post_id: post.dataset.id})
            }
            fetch('http://127.0.0.1:8000/api/like/', data)
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    post.querySelector('#toggle-like').innerHTML = data.res.liked? 'Liked': 'Like'
                    post.querySelector('#number-likes').innerHTML = data.res.number_likes
                }
            })
        }
    })

    document.querySelector('#toggle-follow').onclick = (e) => {
        const data = {
            method : "POST",
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.cookie.split(';').find( c => c.startsWith('csrftoken')).split('=')[1]
            },
            body: JSON.stringify({
                username: e.target.dataset.username
            })
        }
        fetch('http://127.0.0.1:8000/api/follow/', data)
        .then(res => res.json())
        .then(data => {
            if(data.success) {
                e.target.innerHTML = data.res.following? 'Unfollow': 'Follow'
                document.querySelector('#followers').innerHTML = data.res.followers
            }
        })
    }

})