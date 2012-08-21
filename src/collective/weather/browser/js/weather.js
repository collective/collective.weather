function weatherSetCookie(cookieName,cookieValue,nDays) {
    var today = new Date();
    var expire = new Date();
    if (nDays==null || nDays==0) nDays=1;
        expire.setTime(today.getTime() + 3600000*24*nDays);
        document.cookie = cookieName+"="+escape(cookieValue)
                 + ";expires="+expire.toGMTString();
}

function selectCity() {
    $(".weather-choose-city").click(function(e) {
        e.preventDefault();
        var cityId = $(this).parent().attr("data-city-id");
        var nextCity = $("#current-weather-" + cityId);
        var nextCityImg = $("img", nextCity);
        var nextCityTemp = $(".weather-temp", nextCity);
        var nextCityName =  $("#current-city-"+ cityId +" span").text();
        $("#current-weather img").attr("src", nextCityImg.attr("src"));
        $("#current-weather .weather-temp").text(nextCityTemp.text());
        $("#current-city span").text(nextCityName);
        weatherSetCookie("collective.weather.top_weather", cityId);
        $("#top-weather-viewlet.actionMenu.activated").
            removeClass("activated").addClass("deactivated");
        return false;
    })
}

$(document).ready(function() {
    selectCity();
});
