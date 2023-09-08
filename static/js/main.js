const menu = document.querySelector('.menu')
const navbar = document.querySelector('.nav-items-1')
const navbar_wrapper = document.querySelector('.navbar-wrapper')
const cancel_line = document.getElementById('cancel-line')
const first_line = document.getElementById('first-line')
const second_line = document.getElementById('second-line')
const logo = document.querySelector('.logo')
const nav_link = document.querySelectorAll('.nav-link')
const question_container = document.querySelectorAll('.question-container')
const answer_container = document.querySelectorAll('.answer-container')
const arrow_down = document.querySelectorAll('.uil-angle-down')


window.addEventListener('scroll', ()=>{
    navbar_wrapper.classList.toggle('navbar-scroll-toggle', window.scrollY>50)
})

menu.addEventListener('click', function(){
    navbar.classList.toggle('navbar-toggle')
    cancel_line.classList.toggle('cancel-line-toggle')
    first_line.classList.toggle('first-line-toggle')
    second_line.classList.toggle('second-line-toggle')   
})

question_container.forEach(question => {
    question.addEventListener("click", ()=>{
        handle(question)
        const parent = question.parentNode
        const child = parent.lastChild.previousSibling
        const arrow = question.children.item(1)
        arrow.classList.toggle('arrow-toggle')
        child.classList.toggle('answer-container-toggle')
    })
})

function handle(question1) {
    for (let i = 0; i < question_container.length; i++) {
        const question = question_container[i]
        const parent = question.parentNode
        const child = parent.lastChild.previousSibling
        const arrow = question.children.item(1)
        if (question == question1) {
            continue
        }
        if (child.classList.contains('answer-container-toggle')) {
            child.classList.remove('answer-container-toggle')
        }
        if (arrow.classList.contains('arrow-toggle')) {
            arrow.classList.remove('arrow-toggle')
        }
        
        
    }
}