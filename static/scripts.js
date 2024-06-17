$(document).ready(function() {
    $('#propertyForm').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/',
            data: $(this).serialize(),
            success: function(response) {
                $('#modal-location').text(response.location);
                $('#modal-bed').text(response.bed);
                $('#modal-bath').text(response.bath);
                $('#modal-carport').text(response.carport);
                $('#modal-surface_area').text(response.surface_area);
                $('#modal-building_area').text(response.building_area);
                $('#modal-price').text(response.price);

                $('#resultModal').modal('show');
            }
        });
    });
});
