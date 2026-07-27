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

    // 2. Admin Panel Brand Filter (Fixed version)
    const brandsMap = {
        'M': ['iphone', 'Samsung', 'GooglePixel'],
        'L': ['Apple', 'Hp', 'Dell'],
        'TW': ['Lee', 'Wrangler', 'Raymond'],
        'BW': ['Lee', 'Wrangler', 'Spykar']
    };

    const $categorySelect = $('#id_category');
    const $brandSelect = $('#id_brand');

    if ($categorySelect.length && $brandSelect.length) {
        // Badha original options save kari rakho
        const allBrandOptions = $brandSelect.html();

        function updateBrands() {
            const selectedCat = $categorySelect.val();
            const currentBrandVal = $brandSelect.val();
            
            // Dropdown reset karo
            $brandSelect.html(allBrandOptions);

            if (selectedCat && brandsMap[selectedCat]) {
                $brandSelect.find('option').each(function() {
                    const val = $(this).val();
                    if (val !== "" && !brandsMap[selectedCat].includes(val)) {
                        $(this).remove(); // Je brand category ma na aavti hoy tene remove kari dyo
                    }
                });
            } else {
                $brandSelect.find('option').not(':first').remove();
            }

            // Jo pela select kareli brand hoy to tene select rakho
            if ($brandSelect.find(`option[value="${currentBrandVal}"]`).length > 0) {
                $brandSelect.val(currentBrandVal);
            }
        }

        $categorySelect.on('change', function() {
            updateBrands();
        });

        // Page load thay tyare run karo
        updateBrands();
    }
});