function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: 'POST',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        'headers': {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        console.info(data);
        var cart = document.getElementById('cart-info');
        cart.innerText = `${data.total_quantity}`;
    })
}


function pay() {
    fetch('/payment', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json'
        }
    }).then(res => res.json()).then(data => {
        alert(data.message);
    }).catch(res => {
        console.log(res);
    })
}