$(document).ready(function(){
    $("ul.category").on("click", "a.subcategory", function(){
        var id = $(this).attr("id");
        console.log("The ID of the element is: " + id);
        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: "/home",  // Change this to the appropriate route
            method: "POST",  // Use POST or GET depending on your setup
            data: {
                csrfmiddlewaretoken: csrftoken, 
                subcategoryId: id  // Send the extracted ID
            },
            success: function(data) {
                // Handle the response here if needed
                $('#showCategories').html(data)
                // console.log(data);
            },
            error: function(xhr, status, error) {
                // Handle errors here
                console.error(error);
            }
        });
    });

    
});
$(document).ready(function() {
    $('#signup-form').submit(function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Extract form data
        var username = $('#signup_username').val();
        var email = $('#signup_email').val();
        var password = $('#signup_password').val();
       
        var confirm_password = $('#signup_confirm_password').val();
        alert(confirm_password);
        // Client-side validation
        if (password !== confirm_password) {
            alert('Passwords do not match.');
            return;
        }

        // Prepare data for submission
        var formData = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        };

        // Send AJAX POST request
        $.ajax({
            type: 'POST',
            url: '/signup',  // Replace with the correct URL for your signup view
            data: formData,
            success: function(response) {
                // Handle successful signup
                alert('Signup successful!');
                window.location.href = '/home';  // Redirect to the home page
            },
            error: function(xhr, status, error) {
                // Handle errors
                alert('Error occurred during signup: ' + error);
            }
        });
    });
});


$(document).ready(function () {

    $('#loginbutton').click(function (event) {
        // Prevent default button behavior
        event.preventDefault();

        // Get username and password values
        var username = $('#username').val();
        var password = $('#password').val();
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        // AJAX request
        $.ajax({
            url: '/login', // URL of your login view
            type: 'POST',
            data: {
                'username': username,
                'password': password,
                'csrfmiddlewaretoken': csrftoken // Ensure you have CSRF token in your template
            },
            success: function (response) {
                window.location.href = '/home';
            },
            error: function (xhr, errmsg, err) {
                // If login fails, display error message
                console.log(xhr.status + ": " + xhr.responseText); // Log the error to console
                alert("Login failed. Please check your username and password.");
            }
        });
    });

    $('.modal-footer').on('click', '#resetEmailButton', function(event) {
        
        event.preventDefault();
        var messageElement = $('#resetEmailMessage');
        var email = $('#resetEmail').val();
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        if(!email){
            showMessage(messageElement, 'Please enter your email address.', 'red');
            return;
        }

        $.ajax({
            url: '/reset',  // Update this URL to match your server endpoint
            type: 'POST',
            data: {
                email: email
            },
            success: function(response) {
                if (response.status === 'success') {
                    showMessage(messageElement, response.message, 'green');
                    // Optionally, you can close the modal here
                    $('#exampleModal').modal('hide');
                } else {
                    showMessage(messageElement, response.message, 'red');
                }
            },
            error: function(xhr, status, error) {
                showMessage(messageElement,xhr.responseText, 'red');
            }
        });
        function showMessage(element, message, color) {
            
            element.text(message).css('color', color);
            // Remove message after 3 seconds
            setTimeout(function() {
                element.text('');
            }, 3000);
        }
    });

   });

   $(document).ready(function() {

    $('#resetPasswordButton').click(function(event) {
        event.preventDefault();

        var password = $('#password').val();
        var confirm_password = $('#confirm_password').val();
        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        // Client-side validation
        if (password.length < 8) {
            alert('Password must be at least 8 characters long.');
            return;
        }
        
        if (password !== confirm_password) {
            alert('Passwords do not match.');
            return;
        }
        
        // If validation passes, submit the form via AJAX
        var formData = $('#resetPasswordChange').serialize();
        formData += '&csrfmiddlewaretoken=' + encodeURIComponent(csrftoken);
        $.ajax({
            url: window.location.pathname,  // Use the current URL
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.status === 'success') {
                    alert('Password reset successful.');
                    window.location.href = '/home';
                } else {
                    alert('Password reset failed: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                alert('An error occurred while resetting password: ' + error);
            }
        });
    });
    
    
});


$(document).ready(function () {
    console.log("Document is ready");

    $(".add-to-cart").click(function (e) {
        alert('hello');
        e.preventDefault();
        console.log('Add to cart clicked'); // Debugging log

        var productId = $(this).data('product-id');
        console.log('Product ID:', productId); // Debugging log

        var csrftoken = $("input[name='csrfmiddlewaretoken']").val();
        console.log('CSRF Token:', csrftoken); // Debugging log

        $.ajax({
            type: 'POST',
            url: '/add-to-cart/',  // Ensure this URL matches your Django URL configuration
            data: {
                product_id: productId,
                csrfmiddlewaretoken: csrftoken
            },
            success: function (response) {
                console.log('Success response:', response); // Debugging log
                alert('Product added to cart!');
                // Update the cart count or any other UI changes here
            },
            error: function (error) {
                console.log('Error:', error); // Debugging log
                alert('Something went wrong.');
            }
        });
    });

    // Handle quantity increase
    $(".cart_quantity_up").click(function(e){
        e.preventDefault();
        var productId = $(this).data('product-id');
        updateCartQuantity(productId, 'increase');
    });

    // Handle quantity decrease
    $(".cart_quantity_down").click(function(e){
        e.preventDefault();
        var productId = $(this).data('product-id');
        updateCartQuantity(productId, 'decrease');
    });

    function updateCartQuantity(productId, action) {
        $.ajax({
            type: 'POST',
            url: "/update_cart_quantity/" ,
            data: {
                product_id: productId,
                action: action,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            // success: function(response) {
            //     if (response.message === 'Cart updated') {
            //         var quantityInput = $(".cart_quantity_button a[data-product-id='" + productId + "']").siblings("input.cart_quantity_input");
            //         quantityInput.val(response.quantity);
            //         var totalPriceElement = quantityInput.closest("tr").find(".cart_total_price");
            //         totalPriceElement.text('$' + response.total_price);
            //         var currentSubTotal = $('#sub_total').text();
            //         $('#sub_total').text('$' + response.sub_total);
            //         $('#tax').text('$' + response.per);
            //         $('#total_bill').text('$' + response.bill);
            //         alert('Cart updated');
            //     }
            // },
            success: function(response) {
                if (response.message === 'Cart updated') {
                    var quantityInput = $("[data-product-id=" + productId + "]").closest(".input-spinner").find("input.cart_quantity_input");
                    quantityInput.val(response.quantity);
                    console.log(response);
                    $('.productPrice').value
                    var totalPriceElement = quantityInput.closest("tr").find(".cart_total_price");
                    totalPriceElement.text('$' + response.total_price.toFixed(2));
                    $('#sub_total').text('$' + response.sub_total.toFixed(2));
                    $('#tax').text('$' + response.per.toFixed(2));
                    $('#total_bill').text('$' + response.bill.toFixed(2));
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