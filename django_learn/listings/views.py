
from django.shortcuts import render, redirect
from listings.forms import ContactUsForm, BandForm
from listings.models import Band
from django.core.mail import send_mail


def band_list(request):
    bands = Band.objects.all()
    return render(request, 'listings/band_list.html', 
                  {'bands': bands})


def band_detail(request, band_id): # notez le paramètre id supplémentaire
   band = Band.objects.get(id=band_id)  # nous insérons cette ligne pour obtenir le Band avec cet id
   return render(request,
          'listings/band_detail.html',
         {'band': band}) # nous passons l'id au modèle


def contact(request):
    form = ContactUsForm()  # ajout d’un nouveau formulaire ici
    if request.method == 'POST':
        if form.is_valid():
            send_mail(
            subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['admin@merchex.xyz'],
        )
            return redirect('email-sent')  
        else:
            # créer une instance de notre formulaire et le remplir avec les données POST
            form = ContactUsForm(request.POST)
    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request,
            'listings/contact.html',
            {'form': form})  # passe ce formulaire au gabarit


def email_sent(request):
    return render(request,
            'listings/email_sent.html')


def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            # créer une nouvelle « Band » et la sauvegarder dans la db
            band = form.save()
            # redirige vers la page de détail du groupe que nous venons de créer
            # nous pouvons fournir les arguments du motif url comme arguments à la fonction de redirection
            return redirect('band_detail', band.id)

    else:
        form = BandForm()

    return render(request,
            'listings/band_create.html',
            {'form': form})


def band_change(request, band_id):
            band = Band.objects.get(id=band_id)
            form = BandForm(instance=band)  # on pré-remplir le formulaire avec un groupe existant
            return render(request,
                'listings/band_change.html',
                {'form': form,
                 'id': band_id})


def band_delete(request, band_id):
    band = Band.objects.get(id=band_id)  # nécessaire pour GET et pour POST
    if request.method == 'POST':
        # supprimer le groupe de la base de données
        band.delete()
        # rediriger vers la liste des groupes
        return redirect('band_list')
    return render(request,
                'listings/band_delete.html',
                {'band': band})