function showCityWeather(cityId, cityName){
    var data = {};
    if (cityId !== undefined){
        data = {'city': cityId};
    }

    $.ajax({type: 'POST',
             url: '@@update-weather',
             async : true,
             data: data,
             success: function(results){
                $.ajax({type: 'POST',
                         url: '@@current-weather',
                         async : true,
                         data: data,
                         success: function(results){
                                $("div#current-weather").empty().html(results);
                                if (cityName !== undefined){
                                    $("a#current-city > span").text(cityName);
                                }
                                
                            }
                        });

                }
            });
}

function selectCity() {
    $(".weather-choose-city").click(function(e) {
        e.preventDefault();
        var cityId = $(this).parent().attr("data-city-id");
        var cityName = $(this).parent().attr("data-city-name");

        showCityWeather(cityId, cityName);
    })
}

$(document).ready(function() {
    selectCity();
    showCityWeather();
});
