$(document).ready(function() {
    $(document).on('click','#register',function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        var formData = {
            'first_name': $('#first_name').val(),
            'last_name': $('#last_name').val(),
            'email': $('#email').val(),
            'gender':$('input[name="gender"]').filter(':checked').val(),
            'city': $('#city').val(),
            'country': $('select[name=country]').val(),
            'password': $('#password').val(),
            'password_repeat': $('#password_rep').val()
        };
        $.ajax({
            type: 'POST',
            url: '/register', // Replace with your actual URL
            data: formData,
            dataType: 'json',
            success: function(response) {
                if (response.status == 'success'){

                    console.log(response);
                    alert('Registration successful!');
                }else{
                    console.log(response);
                    
                }
                
            },
            error: function(xhr, status, error) {
                // Handle error response
                

                    console.log(xhr.responseText);
                    console.log('Registration failed: ' + xhr.responseText);
                

            }
        });
    });
});


$(document).ready(function() {
    $(document).on('click','#signin',function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        var formData = {
            
            'email': $('#email').val(),           
            'password': $('#password').val(),
            
            };
        $.ajax({
            type: 'POST',
            url: '/signin', // Replace with your actual URL
            data: formData,
            dataType: 'json',
            success: function(response) {
                // Handle successful response
                if(response.status == "success"){

                    $(".loginmessage").text("Sign in successful!").css({
                        "background-color": "green",
                        "color": "white",
                        "border": "2px solid green",
                        "border-radius": "4px"
                    });
                    setTimeout(function() {
                        window.location.href = "/store";
                    }, 2000);
                }else{
                    
                    $(".loginmessage").text("Invalid Credentials!").css({
                        "background-color": "red",
                        "color": "white",
                        "border": "2px solid red",
                        "border-radius": "4px"
                    }).delay(2000).fadeOut(400, function() {
                        $(this).text(""); // Clear the text content after fading out
                    });
                }

            },
            error: function(xhr, status, error) {
                $(".loginmessage").text("Invalid Credentials!").css({
                    "background-color": "red",
                    "color": "white",
                    "border": "2px solid red",
                    "border-radius": "4px"
                }).delay(2000).fadeOut(400, function() {
                    $(this).text(""); // Clear the text content after fading out
                });
                console.log('signin failed: ' + xhr.responseText);
            }
        });
    });
    $(document).on('click','#reset',function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        var formData = {
            
            'email': $('#resetEmail').val(),           
           
            
            };
        $.ajax({
            type: 'POST',
            url: '/reset', // Replace with your actual URL
            data: formData,
            dataType: 'json',
            success: function(response) {
               if (Response.success == 'success'){

                   console.log(response);
                   alert(response.message)
               }else{
                console.log(response);
                alert(response.message)
               }
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log(xhr.responseText);
                console.log('link does not send to email successful!' + xhr.responseText);
            }
        });
    });
    $('#changerPasswordRest').click(function(event) {
        event.preventDefault(); // Prevent the default form submission
        
        var formData = {
            
            'password': $('#password1').val(),
            'password_repeat': $('#password2').val()        
           
            
            };
            alert($('#password1').val());
        $.ajax({
            type: 'POST',
            url: '/', // Replace with your actual URL
            data: formData,
            dataType: 'json',
            success: function(response) {
               if (Response.success == 'success'){

                   console.log(response);
                   alert(response.message)
               }else{
                console.log(response);
                alert(response.message)
               }
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log(xhr.responseText);
                console.log('link does not send to email successful!' + xhr.responseText);
            }
        });
    });
});

$(document).ready(function(){
    $(document).on('click','.addToCart',function(event){
        event.preventDefault();
        var productId;
        
        if ($('.detailProductId').length) {
            // Car page: Get the product ID from the hidden input field with id 'carProductId'
            productId = $('.detailProductId').val();
        } else {
            // Store page: Get the product ID from the hidden input field closest to the clicked button
            productId = $(this).closest('figcaption').find('.productId').val();
        }

        // Perform AJAX request
        $.ajax({
            url: '/add-to-cart/',
            type: 'POST',
            data: {
                'productId': productId,
                
            },
            success: function(response) {
                // Handle success response
                $('#storePRoducts').html(response.cart_display);
                console.log(response.cart);
                $('.notify').text(response.cart);
                console.log("Product added to cart successfully!");
            },
            error: function(response) {
                // Handle error response
                alert("Error adding product to cart.");
            }
        });
    });
})
$(document).ready(function(){
    $(document).on('click','.removeCartProduct', function(event){
        event.preventDefault();
        
        // Get the cart product ID from the hidden input field closest to the clicked button
        var cartProductId = $(this).closest('td').find('.cartProductId').val();

        // Perform AJAX request to remove the cart product
        $.ajax({
            url: '/remove-from-cart/',
            type: 'POST',
            data: {
                'cartProductId': cartProductId,
                
            },
            success: function(response) {
                
                console.log(response.data);
                // Clear existing content of cartProductDisplay
               a = $('#cartProductDisplay').html();
                // Set the HTML content with the updated cart display
                $('#cartProductDisplay').html(response.cart_display);
                $('.totalPrice').text('$' + response.sub_total.toFixed(2));
                $('.tax').text('$' + response.per.toFixed(2));
                $('.totalBill').text('$' + response.bill.toFixed(2));
                $('.notify').text(response.cart);
                $(this).closest('tr').remove();
            },
            error: function(response) {
                // Handle error response
                alert("Error removing product from cart.");
            }
        });
    });

})

$(document).ready(function() {
    $(document).on('click', '#button-plus', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        updateCartQuantity(productId, 'increase');
    });

    $(document).on('click', '#button-minus', function(e) {
        e.preventDefault();
        var productId = $(this).data('product-id');
        updateCartQuantity(productId, 'decrease');
    });

    function updateCartQuantity(productId, action) {
        $.ajax({
            type: 'POST',
            url: "/update_cart_quantity/",
            data: {
                product_id: productId,
                action: action,
            },
            success: function(response) {
                if (response.message === 'Cart updated') {
                    var quantityInput = $("[data-product-id=" + productId + "]").closest(".input-spinner").find("input.cart_quantity_input");
                    quantityInput.val(response.quantity);
                    console.log(response);
                    var totalPriceElement = quantityInput.closest("tr").find(".productPrice");
                    totalPriceElement.text('$' + response.total_price.toFixed(2));
                    $('.totalPrice').text('$' + response.sub_total.toFixed(2));
                    $('.tax').text('$' + response.per.toFixed(2));
                    $('.totalBill').text('$' + response.bill.toFixed(2));
                    alert('Cart updated');
                }
            },
            error: function(error) {
                console.log(error);
                alert('Something went wrong.');
            }
        });
    }
});

$(document).ready(function() {
    // Attach a click event listener to each dropdown item
    $(document).on('click','.dropdown-item', function() {
        // Get the data-cat-id attribute of the clicked item
        var catId = $(this).data('cat-id');
        // Send the POST request to the home URL
        $.ajax({
            url: '/home',
            type: 'POST',
            data: {
                cat_id: catId
            },
            success: function(response) {
                $('#homeProducts').html(response.data)
                // $('#storePRoducts').html(response.data)
            },
            error: function(xhr, status, error) {
                // Handle any errors from the request
                console.error('Error:', error);
            }
        });
    });
    $(document).on('click','.storeItems', function() {
        // Get the data-cat-id attribute of the clicked item
        var catId = $(this).data('cat-id');
        // Send the POST request to the home URL
        $.ajax({
            url: '/store',
            type: 'POST',
            data: {
                cat_id: catId
            },
            success: function(response) {
                console.log(response.data);
                $('#storePRoducts').html(response.data)
            },
            error: function(xhr, status, error) {
                // Handle any errors from the request
                console.error('Error:', error);
            }
        });
    });
});

$(document).on('click','#applyButton', function() {
    var minValue = $('#minValue').val();
    var maxValue = $('#maxValue').val();

    $.ajax({
        url: '/store',  // Ensure this URL matches your Django URL routing
        type: 'POST',
        data: {
            min_value: minValue,
            max_value: maxValue
        },
        success: function(response) {
           
            console.log(response.data);
            $('#storePRoducts').html(response.data)
           
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });
});
