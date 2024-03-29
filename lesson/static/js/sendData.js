function subscribe(data) {
    var XHR = new XMLHttpRequest();
    var urlEncodedData = "";
    var urlEncodedDataPairs = [];
    var name;

    // Transformez l'objet data en un tableau de paires clé/valeur codées URL.
    for (name in data) {
        urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(data[name]));
    }

    // Combinez les paires en une seule chaîne de caractères et remplacez tous
    // les espaces codés en % par le caractère'+' ; cela correspond au comportement
    // des soumissions de formulaires de navigateur.
    urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

    // Configurez la requête
    XHR.open('POST', 'http://tutor.sylvainboussignac.ovh/search/');
    XHR.responseType = 'json';

    // Ajoutez l'en-tête HTTP requise pour requêtes POST de données de formulaire
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    XHR.onload = function () {
        alert(XHR.response['reponse'])
    };
    // Finalement, envoyez les données.
    XHR.send(urlEncodedData);
    XHR.onloadend = function () {
	location.reload();
    };
}

function deleteLesson(data) {
    if (window.confirm("Voulez-vous vraiment supprimer ce cours ?")) {
        var XHR = new XMLHttpRequest();
        var urlEncodedData = "";
        var urlEncodedDataPairs = [];
        var name;

        // Transformez l'objet data en un tableau de paires clé/valeur codées URL.
        for (name in data) {
            urlEncodedDataPairs.push(encodeURIComponent(name) + '=' + encodeURIComponent(data[name]));
        }

        // Combinez les paires en une seule chaîne de caractères et remplacez tous
        // les espaces codés en % par le caractère'+' ; cela correspond au comportement
        // des soumissions de formulaires de navigateur.
        urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

        // Configurez la requête
        XHR.open('POST', 'http://tutor.sylvainboussignac.ovh/home/');
        XHR.responseType = 'json';

        // Ajoutez l'en-tête HTTP requise pour requêtes POST de données de formulaire
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        XHR.onload = function () {
            alert(XHR.response['reponse'])
        };
        // Finalement, envoyez les données.
        XHR.send(urlEncodedData);
	XHR.onloadend = function () {
	    window.location.href = "http://tutor.sylvainboussignac.ovh/";
	};
    }
}

