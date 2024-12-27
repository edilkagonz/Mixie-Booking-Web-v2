document.addEventListener('DOMContentLoaded', function() {
    // Initialize date picker with enhanced options
    flatpickr("#date", {
        minDate: "today",
        dateFormat: "Y-m-d",
        enableTime: false,
        animate: true,
        disableMobile: false,
        monthSelectorType: "static",
        showMonths: 1,
        prevArrow: "←",
        nextArrow: "→",
        locale: {
            firstDayOfWeek: 1
        },
        onChange: function(selectedDates, dateStr) {
            // Add sparkle effect on date selection
            const input = document.getElementById('date');
            input.classList.add('date-selected');
            setTimeout(() => input.classList.remove('date-selected'), 500);
        }
    });

    // Initialize time picker with enhanced options
    flatpickr("#time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        minTime: "09:00",
        maxTime: "18:00",
        time_24hr: false,
        minuteIncrement: 30,
        onChange: function(selectedDates, dateStr) {
            // Add sparkle effect on time selection
            const input = document.getElementById('time');
            input.classList.add('time-selected');
            setTimeout(() => input.classList.remove('time-selected'), 500);
        }
    });

    // Handle package selection
    document.getElementById('package').addEventListener('change', updatePackageDetails);

    // Fix logo navigation
    document.querySelector('.logo-container').addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = '/';
    });

    // Prevent accidental form submission when clicking logo
    document.querySelector('.logo-container').addEventListener('mousedown', function(e) {
        e.preventDefault();
    });
});

function updatePackageDetails() {
    const packageSelect = document.getElementById('package');
    const detailsDiv = document.getElementById('packageDetails');
    
    const packages = {
        basic: {
            name: 'Basic Fun',
            price: '$199',
            duration: '1 Hour',
            includes: [
                'Balloon Art',
                'Face Painting',
                'Basic Magic Show'
            ]
        },
        premium: {
            name: 'Premium Magic',
            price: '$299',
            duration: '2 Hours',
            includes: [
                'Everything in Basic',
                'Advanced Magic Show',
                'Party Games',
                'Character Performance'
            ]
        },
        deluxe: {
            name: 'Deluxe Party',
            price: '$399',
            duration: '3 Hours',
            includes: [
                'Everything in Premium',
                'Costume Changes',
                'Party Favors',
                'Special Effects'
            ]
        }
    };

    const selected = packages[packageSelect.value];
    
    if (selected) {
        detailsDiv.innerHTML = `
            <div class="package-details">
                <h4>${selected.name}</h4>
                <p><strong>Price:</strong> ${selected.price}</p>
                <p><strong>Duration:</strong> ${selected.duration}</p>
                <h5>Includes:</h5>
                <ul>
                    ${selected.includes.map(item => `<li>${item}</li>`).join('')}
                </ul>
            </div>
        `;
    } else {
        detailsDiv.innerHTML = '<p>Please select a package to see details</p>';
    }
}

document.getElementById('bookingForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        package: document.getElementById('package').value,
        payment: {
            cardName: document.getElementById('cardName').value,
            cardNumber: document.getElementById('cardNumber').value,
            expiry: document.getElementById('expiry').value,
            cvv: document.getElementById('cvv').value
        }
    };

    try {
        // Show loading state
        const button = this.querySelector('button[type="submit"]');
        button.innerHTML = 'Processing... 🔄';
        button.disabled = true;

        // Simulate payment processing (replace with actual payment processing)
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Show success message
        alert('Booking successful! Check your email for confirmation.');
        
        // Reset form
        this.reset();
        
        // Reset button
        button.innerHTML = 'Book & Pay Now';
        button.disabled = false;

    } catch (error) {
        console.error('Booking failed:', error);
        alert('Booking failed. Please try again.');
        
        // Reset button
        button.innerHTML = 'Book & Pay Now';
        button.disabled = false;
    }
});

// Add basic card input formatting
document.getElementById('cardNumber').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.replace(/(\d{4})/g, '$1 ').trim();
    e.target.value = value;
});

document.getElementById('expiry').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.slice(0,2) + '/' + value.slice(2,4);
    }
    e.target.value = value;
});

document.getElementById('cvv').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    e.target.value = value.slice(0,3);
}); 