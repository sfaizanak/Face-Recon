document.addEventListener('DOMContentLoaded',()=>{
    document.querySelector('.loderContainer').style.display = 'none';
});

// window.addEventListener('contextmenu',(event)=>{
//     event.preventDefault();
// });

const loader = () =>{
    document.querySelector('.loderContainer').style.display = 'flex';
    return true;
}