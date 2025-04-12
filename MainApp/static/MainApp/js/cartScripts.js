$(document).ready(function () {
    // Function to update cart via AJAX
    function updateCart(action, element) {
        let id = element.attr("pid");
        let quantityElement = element.siblings("span");

        $.ajax({
            type: "GET",
            url: `/${action}`,
            data: { prod_id: id },
            success: function (data) {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Update quantity and total amount
                quantityElement.text(data.quantity);
                $("#total_amount").text("Rs. " + data.total_amount);
                console.log('total_amount',data.total_amount)
                // Update item quantities in the right summary section
                $(`.cart-item-${id} .cart-qty`).text(data.quantity);
                $(`.cart-item-${id} .cart-subtotal`).text(data.item_total);
            },
            error: function () {
                alert("Error updating cart.");
            }
        });
    }

    // Increment quantity
    $(".plus-cart").click(function () {
        updateCart("pluscart", $(this));
    });

    // Decrement quantity
    $(".minus-cart").click(function () {
        updateCart("minuscart", $(this));
    });
});

$(document).ready(function () {
    $(".remove-cart").click(function (e) {
        e.preventDefault(); // Prevent default action of <a> link

        var id = $(this).attr("pid").toString();
        var eml = this; // Store reference to clicked button

        console.log("Removing product ID:", id);

        $.ajax({
            type: "GET",
            url: "/removecart",
            data: { prod_id: id },
            success: function (data) {
                // Update cart totals dynamically
                $("#amount").text(data.amount);
                $("#total_amount").text(data.total_amount);
                console.log(data);
                console.log("Product removed successfully");

                // Remove the closest cart item container
                $(eml).closest(".cart-remove").remove();

                // If the cart is empty, redirect or show empty cart message
                if (data.cart_count === 0) {
                    window.location.href = "/emptycart";  // Redirect to an empty cart page
                    // OR replace cart content dynamically:
                    // $("#cart-container").html('<h3 class="text-center">Your cart is empty.</h3>');
                }
            },
            error: function () {
                alert("Error removing item from cart.");
            }
        });
    });
});














