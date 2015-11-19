$(function() {
    if (window.innerWidth >= 768) {
        $('#nav').addClass('shorter');
    }
});

function mouseOverCountryGroup(countryCode) {
    $('.' + countryCode).children().css({fill: "rgb(26, 188, 156)", transition: "0.4s"});
    $('.' + countryCode).css({fill: "rgb(26, 188, 156)", transition: "0.4s"});
}

function mouseOutCountryGroup(countryCode) {
    $('.' + countryCode).children().css({fill: "rgb(224, 224, 224)", transition: "0.4s"});
    $('.' + countryCode).css({fill: "rgb(224, 224, 224)", transition: "0.4s"});  
}

function clickCountryGroup(countryCode) {
    $('.' + countryCode).children().attr('style','fill: rgb(50, 118, 177);');
    $('.' + countryCode).attr('style','fill: rgb(50, 118, 177);');
}

function checkIfOtherClass(country, method) {
    var countryCode = ""
    if (country.attr('class').indexOf('pe') > -1) {
        countryCode = 'pe'
    } else if (country.attr('class').indexOf('africa') > -1) {
        countryCode = 'africa'
    } else if (country.attr('class').indexOf('sea') > -1) {
        countryCode = 'sea'
    } else if (country.attr('class').indexOf('pacific') > -1) {
        countryCode = 'pacific'
    } else if (country.attr('class').indexOf('mideast') > -1) {
        countryCode = 'mideast'
    } else if (country.attr('class').indexOf('gb') > -1) {
        countryCode = 'gb'
    } else if (country.attr('class').indexOf('kr') > -1) {
        countryCode = 'kr'
    } else if (country.attr('class').indexOf('ru') > -1) {
        countryCode = 'ru'
    } else if (country.attr('class').indexOf('cnx') > -1) {
        countryCode = 'cnx'
    } else if (country.attr('class').indexOf('ceneuro') > -1) {
        countryCode = 'ceneuro'
    } else if (country.attr('class').indexOf('cenamer') > -1) {
        countryCode = 'cenamer'
    }

    if (countryCode != "") {
        switch(method) {
        case 0:
            clickCountryGroup(countryCode);
            break;
        case 1:
            mouseOverCountryGroup(countryCode);
            break;
        case 2:
            mouseOutCountryGroup(countryCode);
            break;
        }
    }
    return countryCode != "";
}




$('.country').on('click', function(e) {
    if (!checkIfOtherClass($(this), 0)) {
        $(this).children().attr('style','fill: rgb(50, 118, 177);');
        $(this).attr('style','fill: rgb(50, 118, 177);');
    }
    var title = $(this).children('title').text();
    if (!title) {
        title = $(this).parent('title').text();
    }
    console.log($(this).children('title').text());
    $.ajax({
        type: "GET",
        url: "/location-changer/",
        data: {
            title: title
        },
        success: function(data) {
            window.location.href = window.location.href.replace('map_view/', data['location'][0])
        }
    });
});

$('.country').on('mouseover', function(e) {
    if (!checkIfOtherClass($(this), 1)) {
        $(this).css({fill: "rgb(26, 188, 156)", transition: "0.4s"});
        $(this).children().css({fill: "rgb(26, 188, 156)", transition: "0.4s"});
    }
});

$('.country').on('mouseout', function(e) {
    if (!checkIfOtherClass($(this), 2)) {
        $(this).css({fill: "rgb(224, 224, 224)", transition: "0.4s"});
        $(this).children().css({fill: "rgb(224, 224, 224)", transition: "0.4s"});
    }
});