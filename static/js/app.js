
let menu_btn = document.querySelector('.menu-btn')
let close_btn = document.querySelector('.close-btn')
let side_bar = document.querySelector('.side_navbar')
let task_cards = document.querySelectorAll('.task')
let search = document.querySelector('.search')
let profile_more = document.querySelector('.profile_more')
let custom_dropdown = document.querySelector('.custom_dropdown')



menu_btn.addEventListener('click', () =>{
    side_bar.style.display = 'inline-block'
    menu_btn.style.display = 'none'
    close_btn.style.display = 'inline-block'
})

close_btn.addEventListener('click', () =>{
    side_bar.style.display = 'none'
    menu_btn.style.display = 'inline-block'
    close_btn.style.display = 'none'
})

profile_more.addEventListener('click', ()=>{
    custom_dropdown.classList.toggle('toggle_custom_dropdown')
    profile_more.classList.toggle('toggle_profile_more')
})
