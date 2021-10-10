function decrementValue(index){
    let form = document.getElementsByTagName("form")[index];
    let value_input = document.getElementsByName("product_quantity")[index-1];
    var value = parseInt(value_input.value, 10);
    value = isNaN(value) ? 0 : value;
    if(value > 0){
        value--;
    }
    value_input.value = value;
    form.submit();
}

function incrementValue(index){
    let form = document.getElementsByTagName("form")[index];
    let value_input = document.getElementsByName("product_quantity")[index-1] 
    var value = parseInt(value_input.value, 10);
    value = isNaN(value) ? 0 : value;
    if(value < 10){
        value++;
    }
    value_input.value = value;
    form.submit();
}