window.onload = () => {
    'use strict';

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .register('/sw.js').then(function (registration) {

            //sw OK
            console.log('ServiceWorker registrato correttamente con scope: ', registration.scope);
        },
            function (err) {

                //errore sw 
                console.log('ServiceWorker fallito: ', err);
            });
    }
}

    
function HideVideo(arrow){
        const titlecnt = arrow.parentElement;
        const videocnt = titlecnt.nextElementSibling;

        if(videocnt){
            videocnt.classList.toggle('hidden');
        }

        arrow.classList.toggle('slide');
}

//function to open and close the Profile menu

function ProfileMenu(){
    const dropdown=document.getElementById('profile_dropdown');
    if(dropdown){
        dropdown.classList.toggle('active_dropdown');
    }
}