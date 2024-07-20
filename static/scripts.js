$(function() {
    var availableCities = [
        "Москва",
        "Санкт-Петербург",
        "Новосибирск",
        // Добавьте остальные города
    ];
    $("#id_city").autocomplete({
        source: availableCities
    });
});
