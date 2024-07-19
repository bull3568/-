


// script.js
let currentIndex = 0;

function moveSlides(n) {
    const slides = document.querySelector('.slides');
    const totalSlides = slides.children.length;

    if (totalSlides === 0) {
        return;  // 슬라이드가 없으면 아무것도 하지 않음
    }

    currentIndex += n;
    console.log(currentIndex)

    if (currentIndex >= totalSlides) {
        currentIndex = 0;
    } else if (currentIndex < 0) {
        currentIndex = totalSlides - 1;
    }

    const offset = -currentIndex * 10;
    slides.style.transform = `translateX(${offset}%)`;
}

function removeCurrentSlide(n) {
    const slides = document.querySelector('.slides');
    const currentSlide = slides.children[0];
    let index_num = currentIndex + 1
    let id_name = '#company_name'+index_num
    console.log(id_name)
    let company_name = $(`${id_name}`).text()
    $.ajax(
        {
            url: "/send_data?_name="+company_name+"&_select="+n,
            method : 'get', 
            dataType : 'text'
        }
    )
    .then(function(result){
        console.log(result)
    })
    if (currentSlide) {
        currentSlide.remove();
        if (currentIndex >= slides.children.length) {
            currentIndex = 0;
        }
        moveSlides(0);  // 슬라이드를 제거한 후 슬라이드의 위치를 재조정
    }
}

function send_data(){

}

// "prev" 버튼 클릭 시 현재 슬라이드를 제거(기업 제거)
document.querySelector('.prev').addEventListener('click', () => {
    removeCurrentSlide(0);
    moveSlides(1);
});

// "next" 버튼 클릭 시 현재 슬라이드를 제거(기업 추가)
document.querySelector('.next').addEventListener('click', () => {
    removeCurrentSlide(1);
    moveSlides(1);
});

// // 자동 슬라이드 기능 (선택사항)
// setInterval(() => {
//     moveSlides(1);
// }, 3000);
