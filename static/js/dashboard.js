const replies_btn = document.querySelectorAll('.replies')
const replies_container = document.querySelectorAll('.reply-container')
const arrow_up = document.querySelector('.uil-angle-up')
const drop_up = document.querySelector('.drop-up')
const go_to_group_btn = document.querySelectorAll('.go-to-group-btn')
const main = document.querySelector('.center')
const menu = document.querySelector('.menu')
const menu_list = document.querySelector('.bi-list')
const cancel = document.querySelector('.bi-x-lg')
const sidebar = document.querySelector('.sidebar')
const selected_group = document.querySelector('.selected-group-section')
const reply_btn = document.querySelectorAll('.reply-btn')
const notification_btn = document.querySelector('.notification-btn')
const notification_wrapper = document.querySelector('.notification-wrapper')
const more_btn = document.querySelectorAll('.more-btn')
const dropdown = document.querySelectorAll('.dropdown')

arrow_up.addEventListener('click', ()=>{
    drop_up.classList.toggle('drop-up-toggle')
    arrow_up.classList.toggle('arrow-up-toggle')
})

replies_btn.forEach(item=>{
    const parent = item.parentNode.parentNode
    const reply_container = parent.childNodes.item(9)
    item.addEventListener('click', () =>{
        reply_container.classList.toggle('reply-container-toggle')
    })  
  
})


menu.addEventListener('click',()=>{
    menu_list.classList.toggle('menu-list-toggle')
    cancel.classList.toggle('cancel-toggle')
    sidebar.classList.toggle('sidebar-toggle')   
})

reply_btn.forEach(item =>{
    item.addEventListener('click', ()=>{
        const parent = item.parentNode.parentNode
        const child = parent.childNodes.item(7)
        console.log(child)
        child.classList.toggle('reply-input-toggle')
    })
})

notification_btn.addEventListener('click', ()=>{
    notification_wrapper.classList.toggle('notification-wrapper-toggle')
})

more_btn.forEach(item =>{
    item.addEventListener('click', ()=>{
        let drop_down = item.parentNode.childNodes
        console.log(drop_down)
        
    })
})

// function handleDropdown() {
//     for (let i = 0; i < dropdown.length; i++) {
//         if (dropdown[i] == sub) {
//             continue
//         }
//         if (dropdown[i].classList.contains('dropdown_toggle')) { 
//             dropdown[i].classList.remove('dropdown_toggle')
//         } 
        
//     }
// }

// function handleDropdown_() {
//     for (let i = 0; i < dropdown.length; i++) {
//         if (dropdown[i].classList.contains('dropdown_toggle')) { 
//             dropdown[i].classList.remove('dropdown_toggle')
//         } 
        
//     }
// }



    
// card_menu.forEach(menu => {
//     menu.addEventListener('click', () => {
//         parent = menu.parentNode
//         sub = parent.children.item(2)
//         sub.classList.toggle('dropdown_toggle') 
//         handleDropdown()
       
//     })
// })

