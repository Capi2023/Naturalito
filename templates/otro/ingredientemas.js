function agregarAlCarrito(bebidaId) {
    var ingredientesSection = document.getElementById('ingredientes-' + bebidaId);
    if (ingredientesSection.style.display === "none") {
        // Mostrar la sección de ingredientes
        ingredientesSection.style.display = "block";
        // Realizar solicitud AJAX para obtener ingredientes
        $.ajax({
            url: `/bebida/${bebidaId}/ingredientes/`,
            method: 'GET',
            success: function(response) {
                // Actualizar la sección de ingredientes con los datos recibidos
                var ingredientesHtml = '';
                response.ingredientes.forEach(function(ingrediente) {
                    ingredientesHtml += `<p>${ingrediente}</p>`;
                });
                ingredientesSection.innerHTML = ingredientesHtml;
            },
            error: function(xhr, errmsg, err) {
                console.error('Error al obtener ingredientes:', errmsg);
            }
        });
    } else {
        // Ocultar la sección de ingredientes si ya está visible
        ingredientesSection.style.display = "none";
    }
}
