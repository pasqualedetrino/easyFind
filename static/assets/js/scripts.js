jQuery(document).ready(function() {
	
    /*
        Fullscreen background
    */
    $.backstretch("/static/assets/img/backgrounds/1.jpg");
    
    /*
        Login form validation
    */
    $('.login-form input[type="text"], .login-form input[type="password"], .login-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    $('.login-form').on('submit', function(e) {
    	
    	$(this).find('input[type="text"], input[type="password"], textarea').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    });
    
    /*
        Registration form validation
    */
    $('.registration-form input[type="text"], .registration-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    $('.registration-form').on('submit', function(e) {
    	
    	$(this).find('input[type="text"], textarea').each(function(){
    		if( $(this).val() == "" ) {
    			e.preventDefault();
    			$(this).addClass('input-error');
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    });



    
})


function messaggio()
{
	document.getElementById("registrazioneProd").innerHTML = "<div id=\"disso\" style=\"background-color: green !important;width: 100%;margin-top: 10px;padding: 10px;text-align: center;color: white;font-weight: 500;     opacity:1;     transition:opacity 2000ms;\">Registrazione del prodotto effettuata con successo!<br>Puoi visualizzare il prodotto registrato nella sezione PRODOTTI GIA ESISTENTI</div>";
}

function messaggio2()
{
	document.getElementById("registrazioneProd").innerHTML = "<div id=\"disso\" style=\"background-color: red !important;width: 100%;margin-top: 10px;padding: 10px;text-align: center;color: white;font-weight: 500;     opacity:1;     transition:opacity 4900ms;\">Errore durante la registrazione del prodotto!<br>Il prodotto risulta essere gi&agrave; stato inserito sulla piattaforma<br>Controlla in modo accurato nella sezione PRODOTTI GIA ESISTENTI</div>";
}

setTimeout(function(){
    document.getElementById('disso').className = 'diss';
}, 5000);





