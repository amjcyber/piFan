$(document).ready(function() {
    // Check if there is a hash in the URL
    var hash = window.location.hash;
    if (hash) {
        // Remove 'active' class from all tab links and tab content
        $('#myTab a').removeClass('active');
        $('.tab-pane').removeClass('show active');
        
        // Add 'active' class to the link and content that matches the hash
        $('#myTab a[href="' + hash + '"]').addClass('active');
        $(hash).addClass('show active');
    }

    // Update the URL hash when a tab is clicked
    $('#myTab a').on('click', function (e) {
        window.location.hash = this.hash;
    });
});
