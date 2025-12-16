from django.shortcuts import render

def home(request):
    endpoints = [
        {"name": "S'inscrire", "url": "/auth/registre/"},
        {"name": "Vérifier Email", "url": "/auth/vérifier-email/"},
        {"name": "Connexion", "url": "/auth/connexion/"},
        {"name": "Rafraîchir Token", "url": "/auth/rafraîchir/"},
        {"name": "Profil", "url": "/auth/profil/"},
        {"name": "Utilisateurs (admin)", "url": "/auth/utilisateurs/"},
        {"name": "Envoyer OTP téléphone", "url": "/auth/téléphone/envoyer-otp/"},
        {"name": "Vérifier OTP téléphone", "url": "/auth/téléphone/vérifier-otp/"},
        {"name": "Mot de passe / Réinitialiser", "url": "/auth/mot de passe/réinitialiser/"},
        {"name": "Mot de passe / Réinitialiser confirmer", "url": "/auth/mot de passe/réinitialiser/confirmer/"},
    ]
    return render(request, "home.html", {"endpoints": endpoints})
