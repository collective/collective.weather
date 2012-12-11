function showCityWeather(cityId, cityName){
    var data = {};
    if (cityId !== undefined){
        data = {'city': cityId};
    }

    $.ajax({type: 'POST',
             url: '@@update-weather',
             async : true,
             data: data,
             success: function(results) {
                $.ajax({type: 'POST',
                         url: '@@current-weather',
                         async : true,
                         data: data,
                         success: function(results){
                                $("div#current-weather").parent().html(results);
                        }
                    });
                }
            });
}

function selectCity() {
    $("#current-city").parent().next('.actionMenuContent').mouseleave(function() {
        $(this).toggle();
    });

    $("#current-city").live("click", function(e) {
        $(this).parent().next('.actionMenuContent').toggle();
    });

    $(".weather-choose-city").live("click", function(e) {
        e.preventDefault();
        var cityId = $(this).parent().attr("data-city-id");
        var cityName = $(this).parent().attr("data-city-name");

        showCityWeather(cityId, cityName);
    });
}

$(document).ready(function() {
    selectCity();
    showCityWeather();
});
