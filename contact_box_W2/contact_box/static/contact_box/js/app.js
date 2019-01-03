document.addEventListener("DOMContentLoaded", function () {
    var new_pn = document.getElementById('new_pn');
    var all_phones = document.querySelector('.all_phones');
    console.log('ready!');
    var address_db = document.querySelector('.address_db');
    var address = document.querySelector('.address');
    var inputs = address.querySelectorAll('input');
    var button = document.querySelector('.new_address');
    var btn_submit = document.getElementById('contact_btn');

    button.addEventListener('click', function (event) {
        event.preventDefault();
        if (button.innerText == "select address from database") {
            address_db.style.display = 'inline';
            address.style.display = 'none';
            for (i = 0; i < 3; i++) {
                inputs[i].required = false;

            }
            inputs[2].value= 'x'; //invalid form
            button.innerText = " create new address";

        }
        else {
            event.preventDefault();
            address.style.display = 'inline';
            address_db.style.display = 'none';
            for (i = 0; i < 3; i++) {
                inputs[i].required = true;
            }

            button.innerText = "select address from database";
        }


    });

    // new_pn.addEventListener('click', function () {
    //     console.log('cos tu nie gra');
    //     //new_pn.innerText = 'phone number 2';
    //     var ph2 = document.querySelector('.phone').cloneNode(true);
    //
    //     all_phones.appendChild(ph2);
    //     //all_phones.appendChild();
    // });

});


