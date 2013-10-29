
function showCityWeather(cityId){

    var data = {'city': cityId};

    if (cityId !== undefined){

        $.ajax({type: 'GET',
                url: portal_url + '/@@update-weather',
                async : true,
                data: data,
                success: function(results) {
                    $.ajax({type: 'GET',
                             url: portal_url + '/@@current-weather',
                             async : true,
                             data: data,
                             success: function(results){
                                    $("#top-weather-viewlet .current-weather").parent().html(results);
                                    createCookie("collective.weather.current_city", cityId, 30);
                            }
                        });
                    }
                });
    }
}

function bindSelectCityEvents() {
    $("#current-city").parent().next('.actionMenuContent').mouseleave(function() {
        $(this).hide();
    });

    $("#current-city").live("click", function(e) {
        e.preventDefault();
        $(this).parent().next('.actionMenuContent').toggle();
    });

    $(".weather-choose-city").live("click", function(e) {
        e.preventDefault();
        var city = $(this).parent().attr('data-city-id');
        showCityWeather(city);
        $(this).parent().parent().parent().toggle();
    });
}

function getCurrentCityFromCookie() {
    var cityId = readCookie("collective.weather.current_city");
    return cityId;
}

$(document).ready(function() {
    bindSelectCityEvents();
    var cityId = getCurrentCityFromCookie();

    if (cityId === undefined || cityId === null){
        var elem = document.getElementById('current-city');
        cityId = $(elem).attr('data-city-id');
    }

    showCityWeather(cityId);
});
