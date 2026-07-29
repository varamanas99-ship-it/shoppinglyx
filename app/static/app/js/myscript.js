(function($) {
    $(document).ready(function() {
        // 1. Owl Carousel Code
        $('#slider1, #slider2, #slider3').owlCarousel({
            loop: true,
            margin: 20,
            responsiveClass: true,
            autoplay: true,
            autoplayTimeout: 3500,        
            autoplayHoverPause: true,        
            smartSpeed: 1000,                    
            slideTransition: 'cubic-bezier(0.25, 1, 0.5, 1)', 
            responsive: {
                0: { items: 1, nav: false },
                600: { items: 3, nav: true },
                1000: { items: 5, nav: true }
            }
        });

        
        const brandsMap = {
            'M': ['iphone', 'Samsung', 'GooglePixel'],
            'L': ['Apple', 'Hp', 'Dell'],
            'TW': ['Lee', 'Wrangler', 'Raymond'],
            'BW': ['Lee', 'Wrangler', 'Spykar']
        };

        const $categorySelect = $('#id_category');
        const $brandSelect = $('#id_brand');

        if ($categorySelect.length && $brandSelect.length) {
            const allBrandOptions = $brandSelect.html();

            function updateBrands() {
                const selectedCat = $categorySelect.val();
                const currentBrandVal = $brandSelect.val();
                
                $brandSelect.html(allBrandOptions);

                if (selectedCat && brandsMap[selectedCat]) {
                    $brandSelect.find('option').each(function() {
                        const val = $(this).val();
                        if (val !== "" && !brandsMap[selectedCat].includes(val)) {
                            $(this).remove();
                        }
                    });
                } else {
                    $brandSelect.find('option').not(':first').remove();
                }

                if ($brandSelect.find(`option[value="${currentBrandVal}"]`).length > 0) {
                    $brandSelect.val(currentBrandVal);
                }
            }

            $categorySelect.on('change', function() {
                updateBrands();
            });

            updateBrands();
        }

        // 3. Checkout Plus / Minus Cart AJAX Code (Updated with Delegation)
        $(document).on('click', '.plus-cart', function(){
            var id = $(this).attr("pid").toString();
            $.ajax({
                type: "GET",
                url: "/pluscart/", 
                data: { prod_id: id },
                success: function(data){
                    document.getElementById("quantity-" + id).innerText = data.quantity;
                    document.getElementById("product-price-" + id).innerText = "Price: Rs. " + data.product_total;
                    document.getElementById("totalamount").innerText = "Rs. " + data.totalamount;
                }
            });
        });

        $(document).on('click', '.minus-cart', function(){
            var id = $(this).attr("pid").toString();
            $.ajax({
                type: "GET",
                url: "/minuscart/", 
                data: { prod_id: id },
                success: function(data){
                    document.getElementById("quantity-" + id).innerText = data.quantity;
                    document.getElementById("product-price-" + id).innerText = "Price: Rs. " + data.product_total;
                    document.getElementById("totalamount").innerText = "Rs. " + data.totalamount;
                }
            });
        });
    });
})(django.jQuery);